import logging as log
from fastapi import APIRouter, Depends

import error
import router.response_class.comments as response
from router.response_class.auth_class import ErrorAuth
import router.request_class.comments as request
from fastapi.responses import JSONResponse
from app.user import get_current_user, User
import app.comments as app
from router.response_class.auth_class import ErrorUNAUTHORIZED

router = APIRouter(
    prefix="/v1",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)


@router.get('/comments', response_model=response.Comments, responses={401: {"model": ErrorUNAUTHORIZED}})
async def get_comments_list(ad: request.Get_comments_list, current_user: User = Depends(get_current_user)):
    log.info("GET - /comments - init")
    comments = app.get_comments_list(ad)
    log.info("/comments - correct get list comments")
    return response.Comments(comments=comments)


@router.post('/comments', response_model=response.Comment,
             responses={404: {"model": response.CommentsNotFound}, 401: {"model": ErrorUNAUTHORIZED}})
async def add_comment(new_comment: request.Add_comment, current_user: User = Depends(get_current_user)):
    log.info("POST - /comments - init")
    comment = app.add_comments(new_comment, current_user)
    if comment == error.ErrNotFoundAd:
        log.error("/comments - ErrNotFoundAd")
        return JSONResponse(status_code=404, content={"message": error.ErrNotFoundAd})
    log.info("/comments - correct create comments")
    return response.Comment(id=comment.id, text=comment.text, user_id=comment.user_id, ad_id=comment.ad_id)


@router.delete('/comments/{id}', response_model=response.Comment,
               responses={403: {"model": ErrorAuth}, 401: {"model": ErrorUNAUTHORIZED}})
async def del_comments(id: str, current_user: User = Depends(get_current_user)):
    log.info("DELETE - /comments - init")
    comment = app.del_comments(id, current_user)
    if comment == error.ErrAccessDeniedComments:
        log.error("/comments - ErrAccessDeniedComments")
        return JSONResponse(status_code=403, content={"message": error.ErrAccessDeniedComments})
    log.info("/comments - correct delete comments")
    return response.Comment(id=comment.id, text=comment.text, user_id=comment.user_id, ad_id=comment.ad_id)
