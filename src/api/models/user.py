from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel

from helpers.authentication import verify_password, get_hash_password
from repositories.postgres import users as user_repository


class UserBase(BaseModel):
    id: Optional[int]
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    created_at: Optional[str]

    def hash_password(self):
        self.password = get_hash_password(self.password)


class UserLogin(UserBase):
    username: Optional[str]
    email: Optional[str]
    username_or_email: str
    password: str

    def validate_user(self):
        user = user_repository.get(self.username_or_email)
        if not user or not verify_password(self.password, user[0]["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        self.id = user[0]["id"]
        return True
