from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title = "shorter is better"
    log_level = "INFO"

    # postgres
    postgres_user = "postgres"
    postgres_pass = "2486"
    postgres_host = "localhost"
    postgres_port = "5432"
    postgres_database = "shortener"

    # kafka
    kafka_db_updater_topic = "shortener_view"
    kafka_db_updater_consumer_count = 1
    kafka_db_updater_group = "shortener_worker"

    KAFKA_ADDRESS = "localhost:9095"

    # redis
    redis_host = "localhost"
    redis_port = 6379
    redis_db: int = 0

    # auth
    access_token_expire_minutes = 30

    debug = True

    class Config:
        case_sensitive = False
        # env_file = '../.env'
        # env_file_encoding = 'utf-8'


config = Settings()
