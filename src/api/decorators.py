from fastapi import Header, HTTPException
from fastapi import status
# from functools import wraps

from helpers.authentication import get_current_user


async def get_user_id_from_token(authorization: str = Header(...)):
    user_id = get_current_user(authorization)
    if user_id:
        return user_id

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid authorization header")


# def login_required(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         token = kwargs['authorization']
#         if get_current_user(token):
#             return f(*args, **kwargs)
#         else:
#             raise HTTPException(status_code=401, detail="Unauthorized user")
#
#     return wrapper
