import logging as log
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import app.user as app
import error
import router.response_class.user as response
import router.request_class.user as request
from router.response_class.auth_class import ErrorUNAUTHORIZED

router = APIRouter(
    prefix="/v1",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.get('/user', response_model=response.UserList, responses={401: {"model": ErrorUNAUTHORIZED}})
async def get_user_list(current_user: app.User = Depends(app.get_current_user)):
    log.info("Get /user - init")
    l_user = app.get_user_list(current_user)
    log.info("/user - finish")
    return response.UserList(users=l_user)


@router.get('/user/{id}', response_model=response.User,
            responses={404: {"model": response.UserNotFound}, 401: {"model": ErrorUNAUTHORIZED}})
async def get_user(id: str, current_user: app.User = Depends(app.get_current_user)):
    log.info("Get /user - init")
    user = app.get_user_for_id(id, current_user)
    if user == error.ErrNotFoundUser:
        log.error("Get /user - ErrNotFoundUser")
        return JSONResponse(status_code=404, content={"message": error.ErrNotFoundUser})
    log.info("Get /user - finish")
    return response.User(id=user.id, name=user.name, surname=user.surname, email=user.email)


@router.put('/user/{id}', response_model=response.User,
            responses={404: {"model": response.UserNotFound}, 401: {"model": ErrorUNAUTHORIZED},
                       403: {"model": response.AccessDeniedUser}})
async def update_user(id: str, update_user: request.update_user,
                      current_user: app.User = Depends(app.get_current_user)):
    log.info("Put /user - init")
    user = app.update_user(id, update_user, current_user)
    if user == error.ErrNotFoundUser:
        log.error("Put /user - ErrNotFoundUser")
        return JSONResponse(status_code=404, content={"message": error.ErrNotFoundUser})
    if user == error.ErrAccessDeniedUser:
        log.error("Put /user - ErrAccessDeniedUser")
        return JSONResponse(status_code=403, content={"message": error.ErrAccessDeniedUser})
    log.info("Put - /user - finish")
    return response.User(id=user.id, name=user.name, surname=user.surname, email=user.email, is_admin=user.is_admin,
                         is_active=user.is_active)
