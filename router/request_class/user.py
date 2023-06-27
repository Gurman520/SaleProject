from pydantic import BaseModel


class update_user(BaseModel):
    name: str | None
    surname: str | None
    email: str | None
    is_admin: bool | None
    is_active: bool | None
