# coding:utf-8
from app import db
from . import bp
from app.models.message import Message
from flask import request, g, current_app
from cerberus import Validator
from json import dumps


V = Validator()
V.allow_unknown = True


@bp.route('/messages', methods=['POST'])
def create_message():
    user = g.current_user
    if user.identity == 0:
        return {'errmsg': '没有权限发布通知', 'errcode': 401}, 401
    data = request.get_json()
    schema = {
        'content': {'type': 'string'},
        'pic': {'type': 'list'}
    }
    if V.validate(data, schema) is False:
        return {'errmsg': '参数出错，请重新检查', 'errmsg': 400}, 400
    images = list(map(lambda x: current_app.config['IMG_BASE_URL'] + x, data['pic']))
    try:
        msg = Message(content=data['content'], pic=dumps(images), user=user)
        db.session.add(msg)
        db.session.commit()
    except:
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '发布消息成功', 'errcode': 200}, 200
