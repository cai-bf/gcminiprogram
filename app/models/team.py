# coding:utf-8
from app import db
import datetime


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    num = db.Column(db.Integer, nullable=False)
    opinion = db.Column(db.Text(3000), comment='看法')
    demand = db.Column(db.Text(3000), comment='要求')
    success = db.Column(db.Integer, default=0)
    poster = db.Column(db.String(255))
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    members = db.relationship('Member', backref='team', lazy='dynamic')
