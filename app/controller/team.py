# coding:utf-8
from . import bp
from flask import g, request, current_app
from app import db
from json import dumps
from app.models import competition, user, team, member, school
from cerberus import Validator
from datetime import datetime


V=Validator()
V.allow_unknown=True

@bp.route('/team', methods=['POST'])
def create_team():
    u = g.current_user
    data=request.get_json()
    schema = {
        'teamname': {'type': 'string'},
        'num': {'type': 'integer'},
        'opinion': {'type': 'integer','required': False},
        'demand': {'type': 'integer', 'required': False},
        'poster': {'type': 'list'},
        'competition_id': {'type': 'integer'},
        'name': {'type': 'string'},
        'school_id': {'type': 'integer'},
        'grade': {'type': 'string'},
        'number': {'type': 'string'},
        'phone': {'type': 'string'},
        'mail': {'type': 'string'}
    }
    if V.validate(data, schema) is False:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    images = data['poster'] if data.get('poster') is not None else []
    images = list(map(lambda x: current_app.config['IMG_BASE_URL'] + x, images))
    s = school.School.query.get(data['school_id'])
    c = competition.Competition.query.get(data['competition_id'])
    if s is None or c is None:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    try:
        t = team.Team(
            name=data['teamname'],
            user=u,
            num=data['num'],
            opinion=data['opinion'],
            demand=data['demand'],
            poster=dumps(images),
            competition=c
        )
        db.session.add(t)
        db.session.commit()
        m = member.Member(
            team=t,
            user=u,
            school=s,
            name=data['name'],
            grade=data['grade'],
            number=data['number'],
            phone=data['phone'],
            mail=data['mail'],
            approved=1
        )
        db.session.add(m)
        db.session.commit()
    except:
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '创建战队成功', 'errcode': 200}, 200

@bp.route('/team', methods=['GET'])
def get_team():

    pass

@bp.route('/team/join', methods=['POST'])
def join_team():
    u = g.current_user
    data=request.get_json()
    schema = {
        'team_id': {'type': 'integer'},
        'name': {'type': 'string'},
        'school_id': {'type': 'integer'},
        'grade': {'type': 'string'},
        'number': {'type': 'string'},
        'phone': {'type': 'string'},
        'mail': {'type': 'string'},
        'remark':{'type':'string','required': False}
    }
    if V.validate(data, schema) is False:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    s = school.School.query.get(data['school_id'])
    t = team.Team.query.get(data['competition_id'])
    if s is None or t is None:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    try:
        m = member.Member(
            team=t,
            user=u,
            school=s,
            name=data['name'],
            grade=data['grade'],
            number=data['number'],
            phone=data['phone'],
            mail=data['mail'],
            identify=1,
            remark=data['remark'],
        )
        db.session.add(m)
        db.session.commit()
    except:
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '加入战队申请成功', 'errcode': 200}, 200

    pass


@bp.route('/team/direct', methods=['POST'])
def create_team_direct():
    u = g.current_user
    data=request.get_json()
    schema = {
        'teamname': {'type': 'string'},
        'num': {'type': 'integer'},
        'competition_id': {'type': 'integer'},
        'leader': {'type': 'string'},
        'school_id': {'type': 'integer'},
        'grade': {'type': 'string'},
        'number': {'type': 'string'},
        'phone': {'type': 'string'},
        'mail': {'type': 'string'},
        'memberlist': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'name': {'type': 'string'},
                    'school_id': {'type': 'integer'},
                    'grade': {'type': 'string'},
                    'number': {'type': 'string'},
                    'phone': {'type': 'string'},
                    'mail': {'type': 'string'},
                }
            }
        }
    }
    if V.validate(data, schema) is False:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    images = data['poster'] if data.get('poster') is not None else []
    images = list(map(lambda x: current_app.config['IMG_BASE_URL'] + x, images))
    s = school.School.query.get(data['school_id'])
    c = competition.Competition.query.get(data['competition_id'])
    if s is None or c is None:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    try:
        t = team.Team(
            name=data['teamname'],
            user=u,
            num=data['num'],
            competition=c
        )
        db.session.add(t)
        db.session.commit()

        l = member.Member(
            team=t,
            user=u,
            school=s,
            name=data['leader'],
            grade=data['grade'],
            number=data['number'],
            phone=data['phone'],
            mail=data['mail'],
            approved=1
        )
        db.session.add(l)
        memberlist = data['memberlist']
        for m in memberlist:
            m_number = m['number']
            m_user = user.User.query.filter_by(number=m_number).first()
            m_u = None if m_user is None else m_user
            m_m = member.Member(
                team=t,
                user=m_u,
                school=s,
                name=m['name'],
                grade=m['grade'],
                number=m['number'],
                phone=m['phone'],
                mail=m['mail'],
                approved=1
            )
            db.session.add(m_m)
        db.session.commit()
    except:
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '创建战队成功', 'errcode': 200}, 200

