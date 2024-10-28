import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://zhaosier:qwe123@localhost:5432/IT_database')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
