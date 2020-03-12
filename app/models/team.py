# coding:utf-8
from app import db
import datetime
from json import loads


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    num = db.Column(db.Integer, nullable=False)
    opinion = db.Column(db.Text(3000), comment='看法')
    demand = db.Column(db.Text(3000), comment='要求')
    success = db.Column(db.Integer, default=0)
    poster = db.Column(db.String(255))
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    members = db.relationship('Member', backref='team', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)

    def get_members(self):
        mlist = self.members
        return [m.to_dict() for m in mlist]

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user.to_dict(),
            'num': self.num,
            'opinion': self.opinion,
            'demand': self.demand,
            'success': self.success,
            'poster': loads(self.poster),
            'competition_id': {
                    'id': self.competition.id,
                    'title': self.competition.title
                },
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
