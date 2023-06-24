from pydantic import BaseModel


class add_new_ad(BaseModel):
    category: str
    title: str
    price: int
    description: str
