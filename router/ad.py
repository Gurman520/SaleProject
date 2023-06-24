import logging as log
from fastapi import APIRouter, Depends
from app.user import get_current_user, User
import router.request_class.ad as request_ad
import router.response_class.ad as response_ad

router = APIRouter(
    prefix="/v1",
    tags=["announcements"],
    responses={404: {"description": "Not found"}},
)


@router.post("/announcement", response_model=response_ad.announcement, status_code=201)
async def add_new_ad(ad: request_ad.add_new_ad, current_user: User = Depends(get_current_user)):
    pass


@router.get("/announcement", response_model=response_ad.ad_list)
async def get_list_ad(current_user: User = Depends(get_current_user)):
    pass


@router.get("/announcement/{id}", response_model=response_ad.announcement)
async def get_ad(id: str, current_user: User = Depends(get_current_user)):
    pass


@router.put("/announcement/{id}", response_model=response_ad.announcement)
async def update_ad(id: str, current_user: User = Depends(get_current_user)):
    pass


@router.delete("/announcement/{id}", response_model=response_ad.announcement)
async def delete_ad(id: str, current_user: User = Depends(get_current_user)):
    pass
