# coding:utf-8
from app.controller import bp
from flask import g, request, current_app, jsonify, abort, make_response
from app.models import user
from app.utils import auth
from wechatpy import WeChatClient


@bp.route('/check_login', methods=['GET'])
def check_login():
    token = request.headers.get('access_token')
    if token is None:
        return {'errmsg': '请先登录'}, 401
    data = auth.decode_auth_token(token)
    if data == -1 or data == -2:
        return {'errmsg': '请重新登录'}, 401
    return {'errmsg': '身份验证成功'}, 200


@bp.route('/login', methods=['POST'])
def login():
    wx = WeChatClient(current_app.config['APPID'], current_app.config['APP_SECRET'],
                      session=current_app.wx_session)
    # wx = WeChatClient(current_app.config['APPID'], current_app.config['APP_SECRET'])
    js_code = request.form.get('jscode')
    if js_code is None:
        return {'errmsg': '出错， 请重试'}, 401
    try:
        data = wx.wxa.code_to_session(js_code)
        openid = data['openid']
        u = user.check_user_by_openid(openid)
        if u is None:
            u = user.create_user(openid)
        u = u.to_dict()
        if 'openid' in u:
            del u['openid']
        return u
    except Exception as e:
        return {'errmsg': str(e)}, 401


@bp.before_app_request
def before_request():
    if request.path == '/check_login' or request.path == 'login':
        return
    token = request.headers.get('access_token')
    if token is None:
        abort(make_response({'errmsg': '还没有登录哦'}, 401))
    data = auth.decode_auth_token(token)
    if data == -1 or data == -2:
        abort(make_response({'errmsg': '还没有登录哦'}, 401))
    g.current_user = user.check_user_by_id(data['id'])

