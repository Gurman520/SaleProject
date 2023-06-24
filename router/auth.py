import logging as log
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import router.response_class.auth_class as response
import router.request_class.auth_class as request
import app.user as app
import db.user as db

router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login", response_model=response.Token, responses={400: {"model": response.ErrorAuth}})
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    token = app.login(form_data)

    if token is None:
        return JSONResponse(status_code=404, content={"message": "User with Email not found"})
    if token == 401:
        return JSONResponse(status_code=401, content={"message": "Could not validate credentials"})
    return response.Token(access_token=token, token_type="bearer")


@router.post("/sign-up", response_model=response.Token, responses={400: {"model": response.ErrorAuth}})
async def create_user(user: request.UserCreate):
    token = app.create(user)
    # проверка существования пользователя
    if token is None:
        return JSONResponse(status_code=400, content={"message": "Email already registered"})
    return response.Token(access_token=token, token_type="bearer")
