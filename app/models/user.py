# coding:utf-8
from app import db
from sqlalchemy.dialects.mysql import TINYINT
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    openid = db.Column(db.String(128), index=True)
    identify = db.Column(TINYINT())
    number = db.Column(db.String(20))
    school = db.Column(db.String(30))
    title = db.Column(db.String(30))  # 头衔： 教授，讲师...
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def from_dict(self, data):
        for field in ['name', 'identify', 'number', 'school', 'title']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'identify': self.identify,
            'number': self.number,
            'school': self.school,
            'title': self.title,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


def create_user(openid):
    user = User()
    user.openid = openid
    db.session.add(user)
    db.session.commit()
    return user


def check_user_by_id(id_):
    u = User.query.get(id_)
    return u


def check_user_by_openid(openid):
    u = User.query().filter_by(openid=openid).first()
    return u


def update_user(user, data):
    u = user
    u.from_dict(data)
    db.session.commit()


