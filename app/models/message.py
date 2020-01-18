# coding:utf-8
from app import db
import datetime


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text(3000), nullable=False)
    read = db.Column(db.Integer, default=0, nullable=False)
    pic = db.Column(db.Text(3000))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    reads = db.relationship('Read', backref='message', lazy='dynamic')
