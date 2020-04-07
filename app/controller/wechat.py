# coding:utf-8
from . import bp
from flask import request, current_app
from app import db
from app.models.follower import Follower
from wechatpy import parse_message, WeChatClient
import hashlib


@bp.route('/wechat', methods=['POST', 'GET'])
def wechat_event():
    # 初次接入验证
    sign = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    if check_signature(['fsdf3432csaQQWWEE', timestamp, nonce], sign):
        return request.args.get('echostr')
    return request.args.get('echostr')

    data = request.data
    msg = parse_message(data)
    if msg.type == 'subscribe':
        if Follower.query.filter_by(openid=msg.source).first() is None:
            wx = WeChatClient(current_app.config['APP_ID'], current_app.config['APP_SECRET'],
                              session=current_app.wx_session)
            user_msg = wx.user.get(msg.source)
            new_follower = Follower(openid=msg.source, unionid=user_msg['unionid'])
            db.session.add(new_follower)
            db.session.commit()
        return '欢迎关注～'
    return ''


def check_signature(data, signature):
    data.sort()
    tmp = ''.join(data)
    tmp = hashlib.sha1(tmp.encode('utf-8')).hexdigest()
    if tmp == signature:
        return True
    return False
