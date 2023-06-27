from pydantic import BaseModel


class new_category(BaseModel):
    name: str
    description: str
