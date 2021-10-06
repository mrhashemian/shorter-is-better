from connections.redis import Redis


def get_access_token(keys: list):
    value = Redis.get_key_values(keys)
    if value:
        return value[0].decode("utf-8")
    return None


def set_access_token(key, value, expire_hour: int = None, expire_minutes: int = None):
    Redis.set_keys(key=key, value=value, expire_minutes=expire_minutes, expire_hour=expire_hour)
