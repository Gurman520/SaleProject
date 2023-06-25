from pydantic import BaseModel


class Comment(BaseModel):
    id: int
    text: str
    user_id: int
    ad_id: int


class Comments(BaseModel):
    comments: list[Comment]
