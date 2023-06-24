from pydantic import BaseModel


class announcement(BaseModel):
    id: int
    category: str
    title: str
    price: int
    description: str


class ad_list(BaseModel):
    announcements: list[announcement]
