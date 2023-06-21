from os import getenv


class Config(object):
    DB_PORT = int(getenv('DB_PORT', default=5432))
    DB_HOST = getenv('DB_HOST', default='localhost')
    DB_NAME = getenv('DB_NAME', default='server')
    DB_USER = getenv('DB_USER', default='admin')
    DB_PASSWORD = getenv('DB_PASSWORD', default='admin')
