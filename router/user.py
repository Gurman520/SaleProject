import logging as log
from fastapi import APIRouter, Depends
from app.user import get_current_user, User

router = APIRouter(
    prefix="/v1",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.get('/user')
async def get_user_list(current_user: User = Depends(get_current_user)):
    pass


@router.get('/user/{id}')
async def get_user(id: str, current_user: User = Depends(get_current_user)):
    pass


@router.put('/user/{id}')
async def update_user(id: str, current_user: User = Depends(get_current_user)):
    pass
