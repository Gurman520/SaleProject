import logging as log
from fastapi import APIRouter, Depends
import router.response_class.comments as response
import router.request_class.comments as request
from fastapi.responses import JSONResponse
from app.user import get_current_user, User
import app.comments as app

router = APIRouter(
    prefix="/v1",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)


@router.get('/comments/{id}', response_model=response.Comments)
async def get_comments_list(id: str, current_user: User = Depends(get_current_user)):
    comments = app.get_comments_list(id)
    return response.Comments(comments=comments)


@router.post('/comments', response_model=response.Comment)
async def add_comment(new_comment: request.Add_comment, current_user: User = Depends(get_current_user)):
    comment = app.add_comments(new_comment, current_user)
    return response.Comment(id=comment.id, text=comment.text, user_id=comment.user_id, ad_id=comment.ad_id)


@router.delete('/comments/{id}', response_model=response.Comment)
async def del_comments(id: str, current_user: User = Depends(get_current_user)):
    comment = app.del_comments(current_user)
    return response.Comment(id=comment.id, text=comment.text, user_id=comment.user_id, ad_id=comment.ad_id)
