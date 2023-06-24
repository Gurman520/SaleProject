from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from config import Config
import db.tables as t

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:5432/{Config.DB_NAME}"
)
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
t.Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)


def create_session():
    global session
    return session()
