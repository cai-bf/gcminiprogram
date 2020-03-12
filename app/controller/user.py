# coding:utf-8
from . import bp
from flask import g, request, current_app
from app import db
from app.models import user
from app.models.school import School
from app.models.member import Member
from cerberus import Validator
import datetime

V = Validator()
# V.allow_unknown = True


@bp.route('/user', methods=['GET'])
def get_user():
    u = g.current_user.to_dict()
    return u

# 完善个人信息与辅导员认证
@bp.route('/user/identify', methods=['POST'])
def set_info():
    u = g.current_user
    data = request.get_json()
    schema = {
        'name': {'type': 'string', 'required': True},
        'identify': {'type': 'integer', 'allowed': [0, 1]},
        'number': {'type': 'string', 'required': True, 'minlength': 6, 'maxlength': 12},
        'title': {'type': 'string', 'required': False},
        'school_id': {'type': 'integer', 'required': True, 'min': 1},
        'key': {'type': 'string', 'required': False,'dependencies': {'identify': 1}}
    }
    if V.validate(data, schema) is False:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    if School.query.get(data['school_id']) is None:
        return {'errmsg': '学校id出错，请重新检查', 'errcode': 400}, 400
    if data['identify'] == 1 and data.get('key') is None:
        return {'errmsg': '无授权码', 'errcode': 400}, 400
    key = current_app.config['CERTIFICATION_KEY']
    if data['identify'] == 1 and key != data['key']:
        return {'errmsg': '认证码错误，请重新检查', 'errcode': 403}, 403
    try:
        data.pop('key')
        user.update_user(u, data)
        if data['identify'] == 0:
            Member.query.filter_by(number=data['number']).update({'user_id':u.id})
    except Exception as e:
        if user.User.query.filter_by(school_id=data['school_id'], number=data['number']).first() is not None:
            return {'errmsg': '该校该学号已注册', 'errcode': 403}, 403
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '更新个人信息成功', 'errcode': 200}, 200

@bp.route('/user/formid', methods=['POST'])
def store_form_id():
    u = g.current_user
    data = request.get_json()
    if data.get('form_id') is None:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    weekday=datetime.date.today().weekday()
    current_app.redis.zset('form_id' + str(weekday), str(u.id) + "_" + data.get('form_id'), u.id)
    current_app.redis.expire('form_id' + str(weekday), 3600 * 24 * 7)
    return {'errmsg': '存储成功', 'errcode': 200}, 200