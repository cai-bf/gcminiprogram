# coding:utf-8
from app import db


class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
