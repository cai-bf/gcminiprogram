# coding:utf-8
from app.controller import bp
from flask import g


@bp.route('/user', methods=['GET'])
def get_user():
    u = g.current_user.to_dict()
    return u
