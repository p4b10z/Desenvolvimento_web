import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@127.0.0.1/desenvolvimento_web"
    SQLALCHEMY_TRACK_MODIFICATIONS = False