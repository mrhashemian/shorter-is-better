import json
from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient

from config import config


class Kafka:
    _connection = None
    _admin_client = None

    @classmethod
    def get_admin_client(cls):
        if not cls._admin_client:
            cls._admin_client = KafkaAdminClient(bootstrap_servers=config.KAFKA_ADDRESS)
        return cls._admin_client

    @classmethod
    def set_producer(cls, c_id: int = 0):
        if not cls._connection:
            producer = KafkaProducer(
                client_id=f"kafka-python-producer-{c_id}",
                bootstrap_servers=config.KAFKA_ADDRESS,
                value_serializer=lambda a: json.dumps(a).encode("utf-8"),
                max_block_ms=5000
            )
            cls._connection = producer
        return cls._connection

    @classmethod
    def set_consumer(cls, topic, group_id):
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=config.KAFKA_ADDRESS,
            group_id=group_id,
            value_deserializer=lambda a: json.loads(a),
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            max_poll_records=50,
            max_poll_interval_ms=70000
        )
        return consumer

    @classmethod
    def get_topics(cls):
        return cls.get_admin_client().list_topics()

    @classmethod
    def declare_topics(cls, topic_list):
        topic_list = [a for a in topic_list if a.name not in cls.get_topics()]
        cls.get_admin_client().create_topics(new_topics=topic_list, validate_only=False)

    @classmethod
    def send_message(cls, topic_name: str, message: dict):
        if not cls._connection:
            cls._connection = cls.set_producer()
        cls._connection.send(topic_name, message)
