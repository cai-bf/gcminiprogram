# coding:utf-8
import datetime
from json import loads
from app import db


class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(200), nullable=False)
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

    teams = db.relationship('Team', backref='competition', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'title': self.title,
            'min_num': self.min_num,
            'max_num': self.max_num,
            'apply_start': self.apply_start.strftime('%Y-%m-%d %H:%M:%S'),
            'apply_end': self.apply_end.strftime('%Y-%m-%d %H:%M:%S'),
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'remark': self.remark,
            'poster': loads(self.poster),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }