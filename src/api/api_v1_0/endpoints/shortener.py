from fastapi import APIRouter, Depends
from starlette.requests import Request
from repositories.redis import links as redis_short_link_repository
from api.decorators import get_user_id_from_token
# from api.models.view import View
from config import config
from helpers.url_shortener import generate_short_link
# from helpers.utils import get_time
# from repositories.postgres import short_link as short_link_repository
# from repositories.postgres import view as view_repository
# from user_agents import parse
from connections.kafka import Kafka

router = APIRouter()


@router.post("/")
def link_shortener(url, user_id=Depends(get_user_id_from_token)):
    # if you want each user can short a specific url once
    # short_url = short_link_repository.get_slug_by_url(user_id, url)
    # if short_url:
    #     return {"short_link": f"shortener.example.com/{short_url['slug']}"}
    slug = generate_short_link(url, user_id)
    return {"short_link": f"shortener.example.com/{slug}"}


@router.get("/{slug}")
def get_original_url(slug, request: Request):
    # get link from postgres
    # url = short_link_repository.get_slug_by_name(slug)

    url = redis_short_link_repository.get_link(slug)

    if not url:
        return {"link": "not found"}

    # insert to postgres directly
    # user_agent = parse(request.headers.get("user-agent"))
    # view_params = {
    #     "link_id": short_url["id"],
    #     "browser": user_agent.browser.family,
    #     "platform": None,
    #     "device": f"{user_agent.device.brand} {user_agent.device.family}",
    #     "system": user_agent.os.family,
    #     "ip": request.client.host,
    #     "created_at": get_time(string_format=True)
    # }
    # if user_agent.is_mobile:
    #     view_params["platform"] = "mobile"
    # elif user_agent.is_tablet:
    #     view_params["platform"] = "tablet"
    # elif user_agent.is_pc:
    #     view_params["platform"] = "pc"
    #
    # view = View(**view_params)
    # view_repository.add(**view.__dict__)
    # short_link_repository.update(short_url["id"])

    Kafka.send_message(config.kafka_db_updater_topic,
                       {"link_id": url["id"], "ip": request.client.host,
                        "user_agent": request.headers.get("user-agent")})
    return url["link"]
