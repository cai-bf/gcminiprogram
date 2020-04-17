# coding:utf-8
from . import bp
from flask import g, request, current_app
from app import db
from app.models import user
from app.models.school import School
from app.models.member import Member
from app.models.captcha import Captcha
from cerberus import Validator
import datetime
import random
from sqlalchemy.exc import IntegrityError

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
        'key': {'type': 'string', 'required': False, 'dependencies': {'identify': 1}}
    }
    if V.validate(data, schema) is False:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    if School.query.get(data['school_id']) is None:
        return {'errmsg': '学校id出错，请重新检查', 'errcode': 400}, 400

    if data['identify'] == 1:
        if data.get('key') is None:
            return {'errmsg': '无授权码', 'errcode': 400}, 400
        captcha = Captcha.query.filter_by(deleted=0, code=data.get('key').upper()).first()
        if captcha is None:
            return {'errmsg': '认证码错误，请重新检查', 'errcode': 403}, 403
         
    try:
        if data['identify'] == 1:
            data.pop('key')
            captcha.deleted = 1
        user.update_user(u, data)
        if data['identify'] == 0:
            Member.query.filter_by(number=data['number']).update({'user_id': u.id})
    except IntegrityError:
        return {'errmsg': '该校该学号已注册', 'errcode': 403}, 403
    except:
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '更新个人信息成功', 'errcode': 200}, 200


@bp.route('/user/bind_students', methods=['POST'])
def bind():
    u = g.current_user
    if u.identify != 1:  # 非教师
        return {'errmsg': '没有权限执行该操作', 'errcode': 400}, 400
    data = request.get_json()
    res = []
    already = []
    for number in data['numbers']:
        stu = user.User.query.filter_by(number=number).first()
        if stu is None:
            res.append(number)
        elif stu.teacher.first() is not None:
            already.append(number)
        else:
            u.students.append(stu)
    db.session.add(u)
    db.session.commit()
    if res == [] and already == []:
        return {'errmsg': '绑定学生成功', 'errcode': 200}, 200
    return {'errmsg': '以下学生尚未注册： ' + ("，".join(res) if res else '无') + ' ' + '以下学生以绑定过教师： ' +
                      "，".join(already) if already else '无', 'errcode': 200}, 200


@bp.route('/user/new_captcha', methods=['GET'])
def new_captcha():
    key = request.args.get('key')
    if key is None:
        return {'errmsg': 'no key', 'errcode': 403}, 403
    if key != current_app.config['CERTIFICATION_KEY']:
        return {'errmsg': 'uncorrect key', 'errcode': 403}, 403
    
    l1 = [str(i) for i in range(10)]
    l2 = [chr(i) for i in range(65, 91)]
    code = ''.join(random.sample(l1 + l2, 6))
    try:
        c = Captcha(code=code)
        db.session.add(c)
        db.session.commit()
    except:
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'code': code}, 200