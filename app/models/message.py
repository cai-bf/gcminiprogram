# coding:utf-8
from app import db
import datetime
from json import loads


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(3000), nullable=False)
    read = db.Column(db.Integer, default=0, nullable=False)
    pic = db.Column(db.Text(3000))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    reads = db.relationship('Read', backref='message', lazy='dynamic')

    def to_dict(self, student=False):
        data = {
            'id': self.id,
            'user': self.user.to_dict(),
            'title': self.title,
            'content': self.content,
            'pic': loads(self.pic),
            'time': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'read_num': self.read
        }
        if student is not False:
            data['read'] = False if self.reads.filter_by(id=student).first() is None else True
        return data
