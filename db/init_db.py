from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
import db.tables as t

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:5432/{Config.DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
t.Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)


def create_session():
    """
    Функция создания сессии
    :return: Сессия
    """
    global session
    return session()


def start():
    """
    Функция создания категорий при старте программы
    :return:
    """
    try:
        sess = create_session()
        u1 = t.User(
            name="admin",
            surname="admin",
            email="admin@admin.com",
            password="$2b$12$Rll99f2IV3utn2mnJICGwuW5.yUcMyu0CW5r6siJ2PmcqSGjO9.TS",
            is_admin=True,
        )
        c1 = t.Category(
            name="Продажа",
        )
        c2 = t.Category(
            name="Покупка",
        )
        c3 = t.Category(
            name="Оказание услуг",
        )
        sess.add(u1)
        sess.add(c1)
        sess.add(c2)
        sess.add(c3)
        sess.commit()
    except:
        print("Внесение изменений не требуется")
        return


start()
