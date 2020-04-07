# coding:utf-8
import datetime
from app import db
from sqlalchemy.dialects.mysql import TINYINT


class Captcha(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(6), nullable=False, unique=True)
	deleted=db.Column(TINYINT(),default=0)
	created_at = db.Column(db.DateTime, default=datetime.datetime.now)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
