# coding:utf-8
from . import bp
from flask import g


@bp.route('/user', methods=['GET'])
def get_user():
    u = g.current_user.to_dict()
    return u
