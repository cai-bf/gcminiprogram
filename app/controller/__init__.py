# coding:utf-8
from flask import Blueprint

bp = Blueprint('', __name__)


from . import auth
from . import user
from . import message
from . import attachment
