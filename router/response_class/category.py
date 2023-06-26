from pydantic import BaseModel
import error


class Category(BaseModel):
    id: int
    name: str
    description: str


class List_category(BaseModel):
    categories: list[Category]


class ErrNotFoundCategory(BaseModel):
    message: str = error.ErrNotFoundCategory
