import os


class Config:
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PWD = os.getenv('DB_PWD')
    DB_URI = f'postgresql://{DB_USER}:{DB_PWD}@localhost/{DB_NAME}'
