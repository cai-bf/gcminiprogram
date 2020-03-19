# coding:utf-8
from . import bp
from flask import g, request, current_app
from app import db
from app.models.follower import Follower
from wechatpy import parse_message, WeChatClient


@bp.route('/wechat/subscribe', methods=['POST', 'GET'])
def subscribe():
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
