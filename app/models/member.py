# coding:utf-8
from app import db
from sqlalchemy.dialects.mysql import TINYINT
import datetime


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    grade = db.Column(db.String(10), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    mail = db.Column(db.String(50), nullable=False)
    identify = db.Column(TINYINT(), nullable=False, comment='0:队长， 1：队员')
    remark = db.Column(db.Text(3000))
    approved = db.Column(TINYINT(), default=0, comment='0：未通过，1：通过')
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
