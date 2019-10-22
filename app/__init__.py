from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from redis import Redis
from wechatpy.session.redisstorage import RedisStorage


db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.controller import bp
    app.register_blueprint(bp)

    app.redis = Redis.from_url(app.config['REDIS_URL'])

    app.session_interface = RedisStorage(app.redis)

    return app
