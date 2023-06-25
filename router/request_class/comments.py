from pydantic import BaseModel


class Add_comment(BaseModel):
    text: str
    ad_id: int
