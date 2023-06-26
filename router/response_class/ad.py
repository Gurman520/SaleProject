from pydantic import BaseModel
import error


class announcement(BaseModel):
    id: int
    category_id: int
    title: str
    price: int
    description: str


class ad_list(BaseModel):
    announcements: list[announcement]


class ErrorNotFoundAD(BaseModel):
    message: str = error.ErrNotFoundAd
