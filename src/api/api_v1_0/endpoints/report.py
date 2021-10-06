from fastapi import APIRouter, Depends

from api.decorators import get_user_id_from_token
from typing_extensions import Literal
from repositories.postgres import view as view_repository

router = APIRouter()


@router.get("/get")
def get_link_view_report(time_period: Literal['c', 'd', 'w', 'm'] = None,
                         user_id=Depends(get_user_id_from_token)
                         ):
    return view_repository.get(user_id, time_period)
