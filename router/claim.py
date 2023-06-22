import logging as log
from fastapi import APIRouter

router = APIRouter(
    prefix="/v1",
    tags=["claim"],
    responses={404: {"description": "Not found"}},
)