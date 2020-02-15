# coding:utf-8
from . import bp
from flask import g, request
from cerberus import Validator
from app import db

V = Validator()
# V.allow_unknown = True


@bp.route('/user', methods=['GET'])
def get_user():
    u = g.current_user.to_dict()
    return u


@bp.route('/user/identify', methods=['POST'])
def identify():
    user = g.current_user
    data = request.get_json()
    schema = {
        'name': {'type': 'string', 'required': True},
        'identify': {'type': 'integer', 'allowed': [0, 1]},
        'number': {'type': 'string', 'required': True, 'minlength': 6, 'maxlength': 12},
        'title': {'type': 'string', 'required': False},
        'school_id': {'type': 'integer', 'required': True}
    }
    if V.validate(data, schema) is False:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400

    for k, v in data.items():
        setattr(user, k, v)
    db.session.commit()
    return {'errmsg': '认证成功', 'errcode': 200}, 200
