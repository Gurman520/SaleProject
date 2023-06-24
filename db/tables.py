from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    is_admin = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)
    data_create = Column(DateTime(), default=datetime.now)
    date_update = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

# Добавить описание класса объявление
