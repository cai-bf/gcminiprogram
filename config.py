# coding:utf-8
import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'iuyasfiush*^*k3w2rkasfas'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(os.environ.get('DB_USER'),
            os.environ.get('DB_PWD'), os.environ.get('DB_HOST'), os.environ.get('DB_PORT'), os.environ.get('DB_NAME'))
    APP_MINI_ID = os.environ.get('APP_ID')
    APP_MINI_SECRET = os.environ.get('APP_SECRET')
    APP_ID = os.environ.get('APP_SERVICE_ID')
    APP_SECRET = os.environ.get('APP_SERVICE_SECRET')
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    IMG_BASE_URL = os.environ.get('IMG_BASE_URL')
    CERTIFICATION_KEY = os.environ.get('CERTIFICATION_KEY')
    MSG_TEMPLATE_ID = os.environ.get('MSG_TEMPLATE_ID')
