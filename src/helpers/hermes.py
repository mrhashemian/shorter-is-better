from hermes import Hermes
from hermes.backend.dict import Backend as DictBackend
from hermes.backend.redis import Backend as RedisBackend

from config import config

dict_cache = Hermes(DictBackend)
redis_cache = Hermes(RedisBackend, host=config.redis_host, port=config.redis_port, db=1)
