import logging as log
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import error
import router.request_class.category as request
import router.response_class.category as response
from router.response_class.auth_class import ErrorAuth
from app.user import get_current_user, User
from router.response_class.auth_class import ErrorUNAUTHORIZED
import app.category as app

router = APIRouter(
    prefix="/v1",
    tags=["category"],
    responses={404: {"description": "Not found"}},
)


@router.get('/category', response_model=response.List_category, responses={401: {"model": ErrorUNAUTHORIZED}})
async def get_category(current_user: User = Depends(get_current_user)):
    log.info("GET - /category - init")
    list_category = app.get_category_list()
    log.info("/category - correct get list category")
    return response.List_category(categories=list_category)


@router.post('/category', response_model=response.Category,
             responses={403: {"model": ErrorAuth}, 401: {"model": ErrorUNAUTHORIZED}})
async def create_category(new_category: request.new_category, current_user: User = Depends(get_current_user)):
    log.info("POST - /category - init")
    new_cat = app.create_category(new_category, current_user)
    if new_cat == error.ErrAccessDeniedCategory:
        log.error("/category - ErrAccessDeniedCategory")
        return JSONResponse(status_code=403, content={"message": error.ErrAccessDeniedCategory})
    log.info("/category - correct create category")
    return response.Category(id=new_cat.id, name=new_cat.name, description=new_cat.description)


@router.delete('/category/{id}', response_model=response.Category,
               responses={403: {"model": ErrorAuth}, 404: {"model": response.ErrNotFoundCategory},
                          401: {"model": ErrorUNAUTHORIZED}})
async def delete_category(id: str, current_user: User = Depends(get_current_user)):
    log.info("DELETE - /category - init")
    del_cat = app.delete_category(id, current_user)
    if del_cat == error.ErrAccessDeniedCategory:
        log.error("/category - ErrAccessDeniedCategory")
        return JSONResponse(status_code=403, content={"message": error.ErrAccessDeniedCategory})
    if del_cat == error.ErrNotFoundCategory:
        log.error("/category - ErrNotFoundCategory")
        return JSONResponse(status_code=404, content={"message": error.ErrNotFoundCategory})
    log.info("/category - correct delete category")
    return response.Category(id=del_cat.id, name=del_cat.name, description=del_cat.description)
