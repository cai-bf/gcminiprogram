# coding:utf-8
import datetime
import jwt
from flask import current_app


def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=6),
            'iat': datetime.datetime.utcnow(),
            'iss': 'xyt',
            'data': {
                'id': user_id
            }
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY']
        )
    except Exception as e:
        return e


def decode_auth_token(token):
    """
    检查token是否有效
    :param token:
    :return:dict|integer  -1表示过期， -2表示token无效， dict正常
    """
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'])
        if 'data' in payload and 'id' in payload['data']:
            return payload['data']
        else:
            raise jwt.InvalidTokenError
    except jwt.ExpiredSignatureError:
        return -1
    except jwt.InvalidTokenError:
        return -2


