from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, Boolean, orm
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    """
    Класс - таблица Пользователь
    """
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    is_admin = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)
    data_create = Column(DateTime(), default=datetime.now)
    date_update = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class Announcement(Base):
    """
    Класс - таблица Объявление
    """
    __tablename__ = 'announcement'
    id = Column(Integer(), primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    title = Column(String(50), nullable=False)
    price = Column(Integer(), nullable=False)
    description = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    data_create = Column(DateTime(), default=datetime.now)
    date_update = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    user = orm.relation('User')
    category = orm.relation('Category')


class Category(Base):
    """
    Класс - таблица Категория
    """
    __tablename__ = 'category'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)


class Comments(Base):
    """
    Класс - таблица Комментариев
    """
    __tablename__ = 'comments'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    ad_id = Column(Integer, ForeignKey('announcement.id'))
    text = Column(String(500), nullable=False)
    data_create = Column(DateTime(), default=datetime.now)
    user = orm.relation('User')
    announcement = orm.relation('Announcement')
