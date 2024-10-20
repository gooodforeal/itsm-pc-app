from fastapi import APIRouter, Response, Depends

from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.schemas import SUserRegister, SUserAuth

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register/")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(username=user_data.username)
    if user:
        return {"status": "error", "message": "User already exists!"}
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {"status": "ok", "message": "Successful registration!"}


@router.post("/login/")
async def auth_user(user_data: SUserAuth):
    check = await authenticate_user(username=user_data.username, password=user_data.password)
    if check is None:
        return {"status": "error", "message": "Wrong username or password!"}
    access_token = create_access_token({"sub": str(check.id)})
    return {"status": "ok", "message": "Successful registration!", "token": access_token}
