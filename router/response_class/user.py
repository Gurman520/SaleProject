from pydantic import BaseModel
import error


class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    is_admin: bool
    is_active: bool


class UserList(BaseModel):
    users: list[User]


class UserNotFound(BaseModel):
    message: str = error.ErrNotFoundUser


class AccessDeniedUser(BaseModel):
    message: str = error.ErrAccessDeniedUser
