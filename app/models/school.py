# coding:utf-8
from app import db


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    member = db.relationship('Member', backref='school', lazy='dynamic')

    user = db.relationship('User', backref='school', lazy='dynamic')
