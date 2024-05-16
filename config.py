import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abcde'
    DB_SERVER = os.environ.get('DB_SERVER') or 'postgres'
    DB_USER = os.environ.get('DB_USER') or 'user'
    DB_NAME = os.environ.get('DB_NAME') or 'db'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'user'
    DB_PORT = os.environ.get('DB_PORT') or 5432