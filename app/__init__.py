# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from redis import Redis
from wechatpy.session.redisstorage import RedisStorage
from flask_migrate import Migrate
from rq import Queue


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.controller import bp
    app.register_blueprint(bp)

    app.redis = Redis.from_url(app.config['REDIS_URL'])

    app.wx_mini_session = RedisStorage(app.redis, "wechatpymini")

    app.wx_session = RedisStorage(app.redis)

    app.rq = Queue(connection=app.redis, name='xyt-queue')

    return app
