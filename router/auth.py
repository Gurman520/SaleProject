import logging as log
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import router.response_class.auth_class as response
import router.request_class.auth_class as request
import app.user as app

router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login", response_model=response.Token, responses={400: {"model": response.ErrorAuth}})
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    log.info("/login - init")
    token = app.login(form_data)

    if token is None:
        log.error("/login - User with Email not found")
        return JSONResponse(status_code=404, content={"message": "User with Email not found"})
    if token == 401:
        log.error("/login - Could not validate credentials")
        return JSONResponse(status_code=401, content={"message": "Could not validate credentials"})
    log.info("/login - Token create")
    return response.Token(access_token=token, token_type="bearer")


@router.post("/sign-up", response_model=response.Token, responses={400: {"model": response.ErrorAuth}})
async def create_user(user: request.UserCreate):
    log.info("/sign-up - init")
    token = app.create(user)
    if token is None:
        log.error("/sign-up - Email already registered")
        return JSONResponse(status_code=400, content={"message": "Email already registered"})
    log.info("?sign-up - Token create")
    return response.Token(access_token=token, token_type="bearer")
