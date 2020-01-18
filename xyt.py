# coding:utf-8
from app import create_app, db
from app.models.user import User
from app.models.school import School
from app.models.competition import Competition
from app.models.team import Team
from app.models.member import Member
from app.models.message import Message
from app.models.read import Read
import datetime
from app.utils.auth import encode_auth_token


app = create_app()

@app.cli.command('init_token')
def init_token():
    u1 = User(name='辅导员一号', openid='qwewqeqweqwe', identify=1, number='123456', title='辅导员')
    u2 = User(name='学生1号', openid='sdfsdfsdf', identify=0, number='654321', school_id=1)
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()

    token = encode_auth_token(u1.id, 120)
    print('辅导员token: {}'.format(token))
    token = encode_auth_token(u2.id, 120)
    print('学生token: {}'.format(token))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=10000)
