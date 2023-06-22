import logging as log
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    name: str
    surname: str
    email: str
    password: str


@router.post("/login", response_model=Token)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    pass
    # Добавить реализацию проверки существования пользователя
    # user = await users_utils.get_user_by_email(email=form_data.username)
    #
    # if not user:
    #     raise HTTPException(status_code=400, detail="Incorrect email or password")
    #
    # if not users_utils.validate_password(
    #     password=form_data.password, hashed_password=user["hashed_password"]
    # ):
    #     raise HTTPException(status_code=400, detail="Incorrect email or password")
    #
    # return await users_utils.create_user_token(user_id=user["id"])


@router.post("/sign-up", response_model=Token)
async def create_user(user: UserCreate):
    pass
# Добавить логику добавления пользователя
#     db_user = await users_utils.get_user_by_email(email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return await users_utils.create_user(user=user)
#
#
# @router.get("/users/me", response_model=users.UserBase)
# async def read_users_me(current_user: users.User = Depends(get_current_user)):
#     return current_user
