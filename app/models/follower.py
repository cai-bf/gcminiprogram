# coding:utf-8
from app import db


class Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(128), index=True, nullable=False)
    unionid = db.Column(db.String(128), index=True, nullable=True)
