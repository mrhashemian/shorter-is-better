import json

from helpers.utils import get_time
import random
import string
from repositories.postgres import short_link as short_link_repository
from repositories.redis import links as redis_short_link_repository


def generate_short_link(url: str, user_id):
    def generate_random():
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(7))

    random_string = generate_random()

    while short_link_repository.exist_slug(random_string):
        random_string = generate_random()

    data = {
        "user_id": user_id,
        "link": url,
        "slug": random_string,
        "view": 0,
        "created_at": get_time(string_format=True)
    }
    link_id = short_link_repository.add(**data)
    redis_short_link_repository.set_link(random_string, json.dumps({"id": link_id, "link": url}))
    return random_string
