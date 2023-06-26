import logging as log
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import error
import router.request_class.category as request
import router.response_class.category as response
from router.response_class.auth_class import ErrorAuth
from app.user import get_current_user, User
import app.category as app

router = APIRouter(
    prefix="/v1",
    tags=["category"],
    responses={404: {"description": "Not found"}},
)


@router.get('/category', response_model=response.List_category)
async def get_category(current_user: User = Depends(get_current_user)):
    list_category = app.get_category_list()
    return response.List_category(categories=list_category)


@router.post('/category', response_model=response.Category, responses={403: {"model": ErrorAuth}})
async def create_category(new_category: request.new_category, current_user: User = Depends(get_current_user)):
    new_cat = app.create_category(new_category, current_user)
    if new_cat == error.ErrAccessDeniedCategory:
        return JSONResponse(status_code=403, content={"message": error.ErrAccessDeniedCategory})
    return response.Category(id=new_cat.id, name=new_cat.name, description=new_cat.description)


@router.delete('/category/{id}', response_model=response.Category,
               responses={403: {"model": ErrorAuth}, 404: {"model": response.ErrNotFoundCategory}})
async def delete_category(id: str, current_user: User = Depends(get_current_user)):
    del_cat = app.delete_category(id, current_user)
    if del_cat == error.ErrAccessDeniedCategory:
        return JSONResponse(status_code=403, content={"message": error.ErrAccessDeniedCategory})
    if del_cat == error.ErrNotFoundCategory:
        return JSONResponse(status_code=404, content={"message": error.ErrNotFoundCategory})
    return response.Category(id=del_cat.id, name=del_cat.name, description=del_cat.description)
