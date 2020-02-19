# coding:utf-8
import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'iuyasfiush*^*k3w2rkasfas'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(os.environ.get('DB_USER'),
            os.environ.get('DB_PWD'), os.environ.get('DB_HOST'), os.environ.get('DB_PORT'), os.environ.get('DB_NAME'))
    APPID = os.environ.get('APP_ID')
    APP_SECRET = os.environ.get('APP_SECRET')
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    IMG_BASE_URL = os.environ.get('IMG_BASE_URL')
