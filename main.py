import uvicorn
import logging as log
from info import description, tags_metadata
from fastapi import FastAPI
from config import Config

# Соединение с БД

app = FastAPI(
    title="Service for placing ads",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata
)

log.info("Start main server")


@app.get("/Health-Check")
def ping():
    log.info("Get Health-Check")
    return {"Message": "OK"}


if __name__ == "__main__":
    uvicorn.run(app)