import json

from connections.redis import Redis


def get_link(keys: list):
    value = Redis.get_key_values(keys)
    if value:
        return json.loads(value[0])
    return None


def set_link(key, value, expire_hour: int = None, expire_minutes: int = None):
    Redis.set_keys(key=key, value=value, expire_minutes=expire_minutes, expire_hour=expire_hour)
