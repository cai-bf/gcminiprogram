# coding:utf-8
from app import create_app, db
from app.models.user import User
from app.models.school import School
from app.models.competition import Competition
from app.models.team import Team
from app.models.member import Member
from app.models.message import Message
from app.models.read import Read
from app.models.follower import Follower
import datetime
from app.utils.auth import encode_auth_token
import random

app = create_app()


@app.cli.command('init_token')
def init_token():
    n1 = random.randint(100000, 99999999)
    n2 = random.randint(100000, 99999999)
    u1 = User(name='辅导员一号', openid='qwewqeqweqwe', identify=1, number=str(n1), title='辅导员', school_id=1)
    u2 = User(name='学生1号', openid='sdfsdfsdf', identify=0, number=str(n2), school_id=1)
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()

    token = encode_auth_token(u1.id, 120)
    print('辅导员token: {}'.format(token))
    token = encode_auth_token(u2.id, 120)
    print('学生token: {}'.format(token))

@app.cli.command('init_school')
def init_school():
    school_list = [
        '机械与汽车工程学院',
        '建筑学院',
        '土木与交通学院',
        '电力学院',
        '电子与信息学院',
        '自动化科学与工程学院',
        '材料科学与工程学院',
        '化学与化工学院',
        '轻工科学与工程学院',
        '食品科学与工程学院',
        '数学学院',
        '物理与光电学院',
        '工商管理学院',
        '公共管理学院',
        '外国语学院',
        '体育学院',
        '马克思主义学院',
        '计算机科学与工程学院',
        '软件学院',
        '环境与能源学院',
        '生物科学与工程学院',
        '新闻与传播学院',
        '设计学院',
        '法学院',
        '经济与贸易学院',
        '艺术学院',
        '医学院'
    ]
    for name in school_list:
        s = School(name=name)
        db.session.add(s)
    db.session.commit()
    print('学院信息导入完毕')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=10000)
