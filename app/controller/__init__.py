# coding:utf-8
from flask import Blueprint

bp = Blueprint('', __name__)


from app.controller import auth
