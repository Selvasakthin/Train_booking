import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abc123'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Selv%40123@localhost/train_booking"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

   