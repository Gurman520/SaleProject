from pydantic import BaseModel


class Add_comment(BaseModel):
    text: str
    ad_id: int


class Get_comments_list(BaseModel):
    announcement_id: int
