from pydantic import BaseModel


class add_new_ad(BaseModel):
    category_id: int
    title: str
    price: int
    description: str


class update_ad(BaseModel):
    category_id: int | None
    title: str | None
    price: int | None
    description: str | None
