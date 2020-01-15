# coding:utf-8
from app import db


class TeacherStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.Integer, db.ForeignKey('user.id'))
    student = db.Column(db.Integer, db.ForeignKey('user.id'))
