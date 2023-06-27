from pydantic import BaseModel
import error


class Comment(BaseModel):
    id: int
    text: str
    user_id: int
    ad_id: int


class Comments(BaseModel):
    comments: list[Comment]


class CommentsNotFound(BaseModel):
    message: str = error.ErrNotFoundComments
