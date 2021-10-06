from connections.postgres import Postgres
from helpers.query_builder import QueryBuilder
from helpers.hermes import dict_cache


def exist_slug(slug_name: str):
    query = f"""select link from links where slug ='{slug_name}'"""
    result = Postgres.select(query)
    if result and len(result) > 0:
        return True
    return False


@dict_cache(ttl=3600 * 2)
def get_slug_by_name(slug_name: str):
    query = f"""select id, link from links where slug ='{slug_name}'"""
    result = Postgres.select(query)
    if result:
        return result[0]
    return False


def get_slug_by_url(user_id, url):
    query = f"""select slug from links where user_id = {user_id} and link ='{url}'"""
    result = Postgres.select(query)
    if result:
        return result[0]
    return False


def add(**data):
    query = QueryBuilder(table_name="links", **data)
    return Postgres.execute(query.get_insert_query(return_values='id'), fetch_result=True)["id"]


def update(link_id: int):
    query = f"""update links set "view" = "view" + 1, updated_at = current_timestamp
                where id ={link_id}"""
    Postgres.execute(query)
