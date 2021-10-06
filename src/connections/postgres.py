from config import config
import psycopg2
from psycopg2 import extras
import psycopg2.extensions


class Postgres:
    _connection = None

    @classmethod
    def get_db_connection(cls):
        if not cls._connection or cls._connection.closed:
            connection = psycopg2.connect(user=config.postgres_user,
                                          password=config.postgres_pass,
                                          host=config.postgres_host,
                                          port=config.postgres_port,
                                          database=config.postgres_database,
                                          connection_factory=extras.RealDictConnection)
            connection.autocommit = True
            cls._connection = connection
        if cls._connection.status == psycopg2.extensions.STATUS_IN_TRANSACTION:
            cls._connection.rollback()
        return cls._connection

    @classmethod
    def select(cls, query):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    @classmethod
    def execute(cls, query, fetch_result=False):
        result = None
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        if fetch_result:
            result = cursor.fetchone()
        cursor.close()
        return result
