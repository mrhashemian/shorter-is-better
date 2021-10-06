import redis
from datetime import timedelta
from config import config


class Redis:
    _pool = None

    @classmethod
    def get_connection(cls):
        if not cls._pool:
            cls._pool = redis.ConnectionPool(host=config.redis_host,
                                             port=config.redis_port,
                                             db=config.redis_db,
                                             encoding="utf-8")
        return redis.StrictRedis(connection_pool=Redis._pool)

    @classmethod
    def set_keys(cls, key, value, expire_hour: int = None, expire_minutes: int = None):
        try:
            conn = cls.get_connection()
            if expire_minutes:
                conn.setex(key, timedelta(minutes=expire_minutes), value=value)
            if expire_hour:
                conn.setex(key, timedelta(hours=expire_hour), value=value)
            else:
                conn.set(key, value)
        except Exception as ex:
            raise ex

    @classmethod
    def get_key_values(cls, keys: list):
        try:
            conn = cls.get_connection()
            value = conn.mget(keys)
            if value:
                return value
            else:
                return []
        except:
            return []
