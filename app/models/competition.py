# coding:utf-8
import datetime

from app import db


class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    min_num = db.Column(db.Integer, nullable=False)
    max_num = db.Column(db.Integer, nullable=False)
    apply_start = db.Column(db.DateTime, nullable=False, comment='报名开始时间')
    apply_end = db.Column(db.DateTime, nullable=False, comment='报名截止时间')
    start_time = db.Column(db.DateTime, nullable=False, comment='比赛开始时间')
    end_time = db.Column(db.DateTime, nullable=False, comment='比赛截止时间')
    remark = db.Column(db.Text(10000))
    poster = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    teams = db.relationship('Team', backref='competition', lazy='dynamic')
