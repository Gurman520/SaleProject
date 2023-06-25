import logging as log
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.user import get_current_user, User
import app.announcement as app
import router.request_class.ad as request_ad
import router.response_class.ad as response_ad

router = APIRouter(
    prefix="/v1",
    tags=["announcements"],
    responses={404: {"description": "Not found"}},
)


@router.post("/announcement", response_model=response_ad.announcement, status_code=201)
async def add_new_ad(ad: request_ad.add_new_ad, current_user: User = Depends(get_current_user)):
    new_ad = app.create_ad(ad, current_user)
    return response_ad.announcement(id=new_ad.id, category_id=new_ad.category_id, title=new_ad.title,
                                    price=new_ad.price,
                                    description=new_ad.description)


@router.get("/announcement", response_model=response_ad.ad_list)
async def get_list_ad(current_user: User = Depends(get_current_user)):
    l_ad = app.get_list_ad(current_user)
    return response_ad.ad_list(announcements=l_ad)


@router.get("/announcement/{id}", response_model=response_ad.announcement)
async def get_ad(id: str, current_user: User = Depends(get_current_user)):
    get_ad = app.get_ad(id)
    return response_ad.announcement(id=get_ad.id, category_id=get_ad.category_id, title=get_ad.title,
                                    price=get_ad.price,
                                    description=get_ad.description)


@router.put("/announcement/{id}", response_model=response_ad.announcement)
async def update_ad(id: str, current_user: User = Depends(get_current_user)):
    pass


@router.delete("/announcement/{id}", response_model=response_ad.announcement)
async def delete_ad(id: str, current_user: User = Depends(get_current_user)):
    del_ad = app.delete_ad(current_user, id)
    if del_ad is None:
        return JSONResponse(status_code=403, content={"message": "No rights to delete"})
    return response_ad.announcement(id=del_ad.id, category_id=del_ad.category_id, title=del_ad.title,
                                    price=del_ad.price, description=del_ad.description)
