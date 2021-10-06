from connections.postgres import Postgres
from helpers.query_builder import QueryBuilder


def add(**data):
    query = QueryBuilder(table_name="views", **data)
    return Postgres.execute(query.get_insert_query(return_values='id'), fetch_result=True)["id"]


# def get(ip: str, link_id):
#     query = f"""select id from views where link_id = {link_id} and ip ='{ip}'"""
#     result = Postgres.select(query)
#     if result:
#         return result[0]
#     return False


def update(view_id: int):
    query = f"""update views set "count" = "count" + 1, updated_at = current_timestamp
                where id ={view_id}"""
    Postgres.execute(query)


def get(user_id, time_period):
    tp = {
        'd': 1,
        'w': 7,
        'm': 30
    }
    query_1_1 = f"""
        with temp as (
            SELECT l.id, l.link, "count"(*) as view, sum(case when v.platform = 'pc' then 1 else 0 end ) As pc,
            sum(case when v.platform = 'mobile' then 1 else 0 end ) As mobile
            FROM views v
            join links l on v.link_id = l.id
            WHERE l.user_id = {user_id}
            {"and v.created_at BETWEEN CURRENT_DATE::TIMESTAMP and CURRENT_TIMESTAMP" if time_period == 'c' else ""}
            {f"and v.created_at BETWEEN (CURRENT_DATE - {tp[time_period]})::TIMESTAMP and CURRENT_DATE::TIMESTAMP - interval '1 sec'" if time_period and not time_period == 'c' else ""}
            GROUP BY 1, 2
        )
        SELECT link, view, pc, mobile, view-pc-mobile as other
        FROM temp
        ORDER BY id desc
    """
    query_1_2 = f"""
        select l.id, l.link, v.browser, count(*) from views v
        join links l on l.id = v.link_id
        where l.user_id = {user_id}
        {"and v.created_at BETWEEN CURRENT_DATE::TIMESTAMP and CURRENT_TIMESTAMP" if time_period == 'c' else ""}
        {f"and v.created_at BETWEEN (CURRENT_DATE - {tp[time_period]})::TIMESTAMP and CURRENT_DATE::TIMESTAMP - interval '1 sec'" if time_period and not time_period == 'c' else ""}
        group by 1, 2, 3
        order by l.id desc 
    """
    query_2_1 = f"""
        with temp as (
            SELECT l.id, l.link, v.ip, sum(case when v.platform = 'pc' then 1 else 0 end ) As pc,
            sum(case when v.platform = 'mobile' then 1 else 0 end ) As mobile,
            sum(case when v.platform != 'mobile' and v.platform != 'pc' then 1 else 0 end ) As other
            FROM views v
            join links l on v.link_id = l.id
            WHERE l.user_id = {user_id}
            {"and v.created_at BETWEEN CURRENT_DATE::TIMESTAMP and CURRENT_TIMESTAMP" if time_period == 'c' else ""}
            {f"and v.created_at BETWEEN (CURRENT_DATE - {tp[time_period]})::TIMESTAMP and CURRENT_DATE::TIMESTAMP - interval '1 sec'" if time_period and not time_period == 'c' else ""}
            GROUP BY 1, 2, 3
        )
        SELECT link, count(*) as view, sum(case when pc > 0 then 1 else 0 end) pc, sum(case when mobile > 0 then 1 else 0 end) mobile, sum(case when other > 0 then 1 else 0 end) other
        FROM temp
        GROUP BY 1, id
        ORDER BY id desc
    """

    query_2_2 = f"""
        with temp as(
            select l.id, l.link, v.browser, count(*) from views v
            join links l on l.id = v.link_id
            where l.user_id = {user_id}
            {"and v.created_at BETWEEN CURRENT_DATE::TIMESTAMP and CURRENT_TIMESTAMP" if time_period == 'c' else ""}
            {f"and v.created_at BETWEEN (CURRENT_DATE - {tp[time_period]})::TIMESTAMP and CURRENT_DATE::TIMESTAMP - interval '1 sec'" if time_period and not time_period == 'c' else ""}
            group by 2, v.ip, 3, l.id
        )
        SELECT id, link, browser, sum(case when "count" > 0 then 1 else 0 end)
        FROM temp
        GROUP BY 1, 2, 3
        order by id desc
    """

    result_1_1 = Postgres.select(query_1_1)
    result_1_2 = Postgres.select(query_1_2)
    result_2_1 = Postgres.select(query_2_1)
    result_2_2 = Postgres.select(query_2_2)

    return {
        "results_1_1": result_1_1,
        "results_1_2": result_1_2,
        "results_2_1": result_2_1,
        "results_2_2": result_2_2
    }
