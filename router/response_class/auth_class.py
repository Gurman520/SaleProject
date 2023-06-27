from pydantic import BaseModel
from fastapi import Response


class Token(BaseModel):
    access_token: str
    token_type: str


class ErrorAuth(BaseModel):
    message: str


class ErrorUNAUTHORIZED(BaseModel):
    detail: str = "Could not validate credentials"
