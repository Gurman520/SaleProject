from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config(object):
    DB_PORT = int(getenv('DB_PORT', default=5432))
    DB_HOST = getenv('DB_HOST', default='localhost')
    DB_NAME = getenv('DB_NAME', default='server')
    DB_USER = getenv('DB_USER', default='admin')
    DB_PASSWORD = getenv('DB_PASSWORD', default='admin')
    SECRET_KEY = getenv('SECRET_KEY', default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM = getenv('ALGORITHM', default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES', default=30))
