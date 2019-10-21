from app import db
from sqlalchemy.dialects.mysql import TINYINT
import datetime
from app.models.mixin import DictMixin


class User(DictMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    openid = db.Column(db.String(128), index=True)
    identify = db.Column(TINYINT())
    number = db.Column(db.String(20))
    remark = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def from_dict(self, data):
        for field in ['name', 'identify', 'number', 'remark']:
            if field in data:
                setattr(self, field, data[field])


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


