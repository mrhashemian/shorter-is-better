from multiprocessing import Process
from kafka.admin import NewTopic
from api.models.view import View
from config import config
from connections.kafka import Kafka
from user_agents import parse
from repositories.postgres import short_link as short_link_repository
from repositories.postgres import view as view_repository

from helpers.utils import get_time


def run_worker(topic_name, group_name):
    consumer = Kafka.set_consumer(topic_name, group_name)
    while True:
        msg_pack = consumer.poll(timeout_ms=2000, max_records=100)
        if msg_pack is None:
            continue
        try:
            for tp, messages in msg_pack.items():
                for item in messages:
                    user_agent = parse(item.value["user_agent"])
                    view_params = {
                        "link_id": item.value["link_id"],
                        "browser": user_agent.browser.family,
                        "platform": None,
                        "device": f"{user_agent.device.brand} {user_agent.device.family}",
                        "system": user_agent.os.family,
                        "ip": item.value["ip"],
                        "created_at": get_time(string_format=True)
                    }
                    if user_agent.is_mobile:
                        view_params["platform"] = "mobile"
                    elif user_agent.is_tablet:
                        view_params["platform"] = "tablet"
                    elif user_agent.is_pc:
                        view_params["platform"] = "pc"

                    view = View(**view_params)
                    view_repository.add(**view.__dict__)
                    short_link_repository.update(item.value["link_id"])
        finally:
            consumer.commit()


if __name__ == "__main__":
    topic_list = [
        NewTopic(name=config.kafka_db_updater_topic, num_partitions=9, replication_factor=1)
    ]
    Kafka.declare_topics(topic_list)

    consumers = []
    for i in range(config.kafka_db_updater_consumer_count):
        consumers.append((config.kafka_db_updater_topic, config.kafka_db_updater_group))

    all_processes = []
    for consumer in consumers:
        p = Process(target=run_worker, args=consumer)
        p.start()
        all_processes.append(p)

    for process in all_processes:
        process.join()
