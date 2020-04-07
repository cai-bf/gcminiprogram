# coding:utf-8
from app import db
from sqlalchemy.dialects.mysql import TINYINT
import datetime
from .message import Message
from .follower import Follower


teacherStudent = db.Table(
    'teacher_student',
    db.Column('teacher', db.Integer, db.ForeignKey('user.id')),
    db.Column('student', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    openid = db.Column(db.String(128), index=True)
    unionid = db.Column(db.String(128))
    identify = db.Column(TINYINT(), comment='0:学生, 1:教师')
    number = db.Column(db.String(20))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    title = db.Column(db.String(30), comment='头衔：教授，讲师, 辅导员...')
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    __table_args__ = (
        db.UniqueConstraint('number', 'school_id', name='uix_number_school'),
    )

    students = db.relationship('User', secondary=teacherStudent,
                               primaryjoin=(teacherStudent.c.teacher == id),
                               secondaryjoin=(teacherStudent.c.student == id),
                               backref=db.backref('teacher', lazy='dynamic'), lazy='dynamic')

    # follower指用户对应的follower信息
    follower = db.relationship('Follower', backref='user', uselist=False,
                               foreign_keys=[unionid],
                               primaryjoin=(unionid == Follower.unionid))

    competitions = db.relationship('Competition', backref='user', lazy='dynamic')

    teams = db.relationship('Team', backref='user', lazy='dynamic')

    # 我参与的团队
    involvements = db.relationship('Member', backref='user', lazy='dynamic')

    read = db.relationship('Read', backref='user', lazy='dynamic')

    messages = db.relationship('Message', backref='user', lazy='dynamic')

    def from_dict(self, data):
        for field in ['name', 'identify', 'number', 'school_id', 'title']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'identify': self.identify,
            'number': self.number,
            'school': None if self.school is None else self.school.to_dict(),
            'title': self.title,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def get_messages(self, page, per_page=10):
        return self.messages.order_by(Message.created_at.desc()).paginate(page, per_page, error_out=False)


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
    u = User.query.filter_by(openid=openid).first()
    return u


def update_user(user, data):
    u = user
    u.from_dict(data)
    db.session.commit()


