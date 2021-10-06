from connections.postgres import Postgres
from helpers.query_builder import QueryBuilder


def add(**kwargs):
    query = QueryBuilder(table_name="users", schema_name="public", **kwargs)
    return Postgres.execute(query.get_insert_query(return_values='id'), True)['id']


def get(username_or_email):
    query = f"""SELECT * FROM users
                where username = '{username_or_email}'
                or email = '{username_or_email}'"""
    return Postgres.select(query)
