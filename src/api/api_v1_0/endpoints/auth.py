from fastapi import APIRouter, HTTPException

from repositories.redis import users as redis_user_repository
from repositories.postgres import users as user_repository
from api.models.user import UserLogin, UserCreate
from config import config
from helpers.authentication import create_access_token
from helpers.utils import get_time
from datetime import timedelta

router = APIRouter()


@router.post("/login")
def login(user: UserLogin):
    user.validate_user()
    access_token_expires = timedelta(minutes=config.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    redis_user_repository.set_access_token(f"user_id_{user.id}", access_token,
                                           expire_minutes=config.access_token_expire_minutes)
    return {"access_token": access_token, "token_type": "bearer",
            "1": "حافظ چو نافه سر زلفش به دست توست",
            "2": "دم درکش ارنه باد صبا را خبر شود"}


@router.post("/register")
def register(user: UserCreate):
    if user_repository.get(user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    elif user_repository.get(user.email):
        raise HTTPException(status_code=400, detail="email already registered")
    user.hash_password()
    user.created_at = get_time(string_format=True)
    user_id = user_repository.add(**user.dict())
    return {"user_id": user_id,
            "1": "",
            "2": ""}
