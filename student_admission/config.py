import os

class Config:
    SECRET_KEY = 'test@1234'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/StudentManagement'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
