# coding:utf-8
from . import bp
from flask import g, request, current_app
from app import db
from app.models import user, school, member
from cerberus import Validator

V = Validator()
V.allow_unknown = True

@bp.route('/user', methods=['GET'])
def get_user():
    u = g.current_user.to_dict()
    return u

# 完善个人信息
@bp.route('/user', methods=['POST'])
def set_info():
    u = g.current_user
    data = request.get_json()
    schema = {
        'name': {'type': 'string'},
        'number': {'type': 'string'},
        'school_id': {'type': 'integer'},
        'title':{'type':'string','required': False}
    }
    if V.validate(data, schema) is False:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    if school.School.query.get(data['school_id']) is None:
        return {'errmsg': '学校id参数出错，请重新检查', 'errcode': 400}, 400
    try:
        user.update_user(u, data)
        # member 填直接报名的user_id,根据学号查找
        member.Member.query.filter_by(number=data['number']).update({'user_id':u.id})
    except:
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '更新个人信息成功', 'errcode': 200}, 200

# 教师认证（感觉这种方法不太行）
@bp.route('/user/certification', methods=['POST'])
def certificate_teacher():
    u = g.current_user
    data = request.get_json()
    schema = {
        'name': {'type': 'string','required': False},
        'key': {'type': 'string'}
    }
    if V.validate(data, schema) is False:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    key = current_app.config['CERTIFICATION_KEY']
    if key != data['key']:
        return {'errmsg': '认证码错误，请重新检查', 'errcode': 400}, 400
    d = {'identify': 1}
    try:
        user.update_user(u, d)
    except:
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '教师认证成功', 'errcode': 200}, 200 