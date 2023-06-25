import uvicorn
import logging as log
from info import description, tags_metadata
from fastapi import FastAPI
from config import Config
import router.auth as auth
import router.announcement as ad
import router.comments as comment

# Соединение с БД

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


@app.get("/Health-Check")
def ping():
    log.info("Get Health-Check")
    return {"Message": "OK"}


def main():
    uvicorn.run(app)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('Неожиданное завершение программы из-за ошибки:')
        print(e)
