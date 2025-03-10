import os
import pymysql

pymysql.install_as_MySQLdb()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "abc123")
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Selv%40123@localhost/train_booking'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
