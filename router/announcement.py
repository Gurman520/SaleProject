import logging as log
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.user import get_current_user, User
import app.announcement as app
import router.request_class.ad as request_ad
import router.response_class.ad as response_ad
import error

router = APIRouter(
    prefix="/v1",
    tags=["announcements"],
    responses={404: {"description": "Not found"}},
)


@router.post("/announcement", response_model=response_ad.announcement, status_code=201)
async def add_new_ad(ad: request_ad.add_new_ad, current_user: User = Depends(get_current_user)):
    new_ad = app.create_ad(ad, current_user)
    if new_ad == error.ErrNotFoundCategory:
        return JSONResponse(status_code=404, content={"message": error.ErrNotFoundCategory})
    return response_ad.announcement(id=new_ad.id, category_id=new_ad.category_id, title=new_ad.title,
                                    price=new_ad.price,
                                    description=new_ad.description)


@router.get("/announcement", response_model=response_ad.ad_list)
async def get_list_ad(current_user: User = Depends(get_current_user)):
    l_ad = app.get_list_ad()
    return response_ad.ad_list(announcements=l_ad)


@router.get("/announcement/{id}", response_model=response_ad.announcement,
            responses={404: {"model": response_ad.ErrorNotFoundAD}})
async def get_ad(id: str, current_user: User = Depends(get_current_user)):
    get_ad = app.get_ad(id)
    if get_ad == error.ErrNotFoundAd:
        return JSONResponse(status_code=404, content={"message": error.ErrNotFoundAd})
    return response_ad.announcement(id=get_ad.id, category_id=get_ad.category_id, title=get_ad.title,
                                    price=get_ad.price,
                                    description=get_ad.description)


@router.put("/announcement/{id}", response_model=response_ad.announcement,
            responses={404: {"model": response_ad.ErrorNotFoundAD}})
async def update_ad(id: str, ad: request_ad.update_ad, current_user: User = Depends(get_current_user)):
    update_ad = app.update_ad(id, ad, current_user)
    if update_ad == error.ErrNotFoundCategory:
        return JSONResponse(status_code=404, content={"message": error.ErrNotFoundCategory})
    return response_ad.announcement(id=update_ad.id, category_id=update_ad.category_id, title=update_ad.title,
                                    price=update_ad.price,
                                    description=update_ad.description)


@router.delete("/announcement/{id}", response_model=response_ad.announcement,
               responses={404: {"model": response_ad.ErrorNotFoundAD}})
async def delete_ad(id: str, current_user: User = Depends(get_current_user)):
    del_ad = app.delete_ad(current_user, id)
    if del_ad == error.ErrNotFoundAd:
        return JSONResponse(status_code=404, content={"message": error.ErrNotFoundAd})
    if del_ad is error.ErrAccessDeniedAd:
        return JSONResponse(status_code=403, content={"message": error.ErrAccessDeniedAd})
    return response_ad.announcement(id=del_ad.id, category_id=del_ad.category_id, title=del_ad.title,
                                    price=del_ad.price, description=del_ad.description)
