import uvicorn
import logging as log
from info import description, tags_metadata
from fastapi import FastAPI
import router.auth as auth
import router.announcement as ad
import router.comments as comment
import router.category as category

log.basicConfig(level=log.INFO, filename="./server_log.log", filemode="a",
                format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(
    title="Service for placing ads",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata
)

log.info("Start main server")
# Подключение эндпоинтов
app.include_router(auth.router)
app.include_router(ad.router)
app.include_router(comment.router)
app.include_router(category.router)


@app.get("/Health-Check")
def ping():
    log.info("Get Health-Check")
    return {"Message": "OK"}


if __name__ == "__main__":
    uvicorn.run(app)
