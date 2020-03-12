# coding:utf-8
from . import bp
from flask import g, request, current_app
from app import db
from json import dumps
from app.models.team import Team
from app.models.competition import Competition
from app.models.user import User
from app.models.member import Member
from app.models.school import School
from cerberus import Validator
from datetime import datetime


V = Validator()
V.allow_unknown = True

# 创建战队
@bp.route('/team', methods=['POST'])
def create_team():
    u = g.current_user
    data = request.get_json()
    schema = {
        'teamname': {'type': 'string'},
        'num': {'type': 'integer'},
        'opinion': {'type': 'string', 'required': False},
        'demand': {'type': 'string', 'required': False},
        'poster': {'type': 'list','required': False},
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
    images = list(
        map(lambda x: current_app.config['IMG_BASE_URL'] + x, images))
    s = School.query.get(data['school_id'])
    c = Competition.query.get(data['competition_id'])
    if s is None or c is None:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    created = Team.query.filter_by(user_id=u.id, competition_id=c.id).count()
    if created != 0:
        return {'errmsg': '请勿重复申请战队', 'errcode': 403}, 403
    if datetime.now() > c.apply_end:
        return {'errmsg': '比赛报名阶段已结束', 'errcode': 403}, 403
    if data['num'] > c.max_num or data['num'] < c.min_num:
        return {'errmsg': '人数不符合比赛要求', 'errcode': 403}, 403
    try:
        t = Team(
            name=data['teamname'],
            user=u,
            num=data['num'],
            opinion=data.get('opinion'),
            demand=data.get('demand'),
            poster=dumps(images),
            competition=c
        )
        db.session.add(t)
        db.session.flush()
        m = Member(
            team=t,
            user=u,
            school=s,
            name=data['name'],
            grade=data['grade'],
            number=data['number'],
            phone=data['phone'],
            mail=data['mail'],
            identify=0,
            approved=1
        )
        db.session.add(m)
        db.session.commit()
    except Exception as e:
        print(e)
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '创建战队成功', 'errcode': 200}, 200

# 加入
@bp.route('/team/join', methods=['POST'])
def join_team():
    u = g.current_user
    data = request.get_json()
    schema = {
        'team_id': {'type': 'integer'},
        'name': {'type': 'string'},
        'school_id': {'type': 'integer'},
        'grade': {'type': 'string'},
        'number': {'type': 'string'},
        'phone': {'type': 'string'},
        'mail': {'type': 'string'},
        'remark': {'type': 'string', 'required': False}
    }
    if V.validate(data, schema) is False:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    s = School.query.get(data['school_id'])
    t = Team.query.get(data['team_id'])
    if s is None or t is None:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    joined = Member.query.filter_by(user_id=u.id, team_id=t.id).count()
    if joined != 0:
        return {'errmsg': '请勿重复申请加入', 'errcode': 403}, 403
    if datetime.now() > t.competition.apply_end:
        return {'errmsg': '比赛报名阶段已结束', 'errcode': 403}, 403
    try:
        m = Member(
            team=t,
            user=u,
            school=s,
            name=data['name'],
            grade=data['grade'],
            number=data['number'],
            phone=data['phone'],
            mail=data['mail'],
            identify=1,
            remark=data.get('remark'),
        )
        db.session.add(m)
        db.session.commit()
    except:
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '加入战队申请成功', 'errcode': 200}, 200

# 直接报名
@bp.route('/team/direct', methods=['POST'])
def create_team_direct():
    u = g.current_user
    data = request.get_json()
    schema = {
        'teamname': {'type': 'string'},
        'num': {'type': 'integer'},
        'competition_id': {'type': 'integer'},
        'opinion': {'type': 'string', 'required': False},
        'demand': {'type': 'string', 'required': False},
        'poster': {'type': 'list','required': False},
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
    images = list(
        map(lambda x: current_app.config['IMG_BASE_URL'] + x, images))
    s = School.query.get(data['school_id'])
    c = Competition.query.get(data['competition_id'])
    if s is None or c is None:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    created = Team.query.filter_by(user_id=u.id, competition_id=c.id).count()
    if created != 0:
        return {'errmsg': '请勿重复申请战队', 'errcode': 403}, 403
    if datetime.now() > c.apply_end:
        return {'errmsg': '比赛报名阶段已结束', 'errcode': 403}, 403
    if data['num'] > c.max_num or data['num'] < c.min_num:
        return {'errmsg': '人数不符合比赛要求', 'errcode': 403}, 403
    try:
        t = Team(
            name=data['teamname'],
            user=u,
            num=data['num'],
            opinion=data.get('opinion'),
            demand=data.get('demand'),
            poster=dumps(images),
            competition=c,
            success=1
        )
        db.session.add(t)
        db.session.flush()
        l = Member(
            team=t,
            user=u,
            school=s,
            name=data['leader'],
            grade=data['grade'],
            number=data['number'],
            phone=data['phone'],
            mail=data['mail'],
            identify=1,
            approved=1
        )
        db.session.add(l)
        memberlist = data['memberlist']
        for m in memberlist:
            m_number = m['number']
            m_user = User.query.filter_by(number=m_number).first()
            m_u = None if m_user is None else m_user
            m_m = Member(
                team=t,
                user=m_u,
                school=s,
                name=m['name'],
                grade=m['grade'],
                number=m['number'],
                phone=m['phone'],
                mail=m['mail'],
                identify=0,
                approved=1
            )
            db.session.add(m_m)
        db.session.commit()
    except Exception as e:
        print(e)
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '直接报名成功', 'errcode': 200}, 200

# 竞赛所有战队
@bp.route('/teams/<int:competition_id>', methods=['GET'])
def get_teams(competition_id):
    page = request.args.get('page', 1, type=int)
    registered = request.args.get('registered', 1, type=int)
    per_page = 10
    t = Team.query.filter_by(competition_id=competition_id, success=registered).order_by(Team.created_at.desc()).paginate(page, per_page, error_out=False)
    return {
        'items': [val.to_dict() for val in t.items],
        'has_next': t.has_next,
        'has_prev': t.has_prev,
        'page': t.page,
        'pages': t.pages,
        'per_page': t.per_page,
        'prev_num': t.prev_num,
        'next_num': t.next_num,
        'total': t.total
    }, 200

# 获取我参与的战队
@bp.route('/teams/my', methods=['GET'])
def get_my_teams():
    u = g.current_user
    page = request.args.get('page', 1, type=int)
    per_page = 10
    t = Member.query.filter_by(user_id=u.id).order_by(Member.created_at.desc()).paginate(page, per_page, error_out=False)
    return {
        'items': [val.team.to_dict() for val in t.items],
        'has_next': t.has_next,
        'has_prev': t.has_prev,
        'page': t.page,
        'pages': t.pages,
        'per_page': t.per_page,
        'prev_num': t.prev_num,
        'next_num': t.next_num,
        'total': t.total
    }, 200

# 获取单个战队
@bp.route('/team/<int:team_id>', methods=['GET'])
def get_team(team_id):
    t = Team.query.get(team_id)
    if t is None:
        return {'errmsg': '此战队不存在', 'errcode': 404}, 404
    return t.to_dict(), 200

# 搜索战队
@bp.route('/team', methods=['GET'])
def search_team():
    name = request.args.get('name')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    if name is None:
        return {'errmsg': '参数错误', 'errcode': 400}, 400
    else:
        t = Team.query.filter(Team.name.like("%"+name+"%")).order_by(Team.created_at.desc()).paginate(page, per_page, error_out=False)
    return {
        'items': [val.to_dict() for val in t.items],
        'has_next': t.has_next,
        'has_prev': t.has_prev,
        'page': t.page,
        'pages': t.pages,
        'per_page': t.per_page,
        'prev_num': t.prev_num,
        'next_num': t.next_num,
        'total': t.total
    }, 200


# 获取成员列表
@bp.route('/team/<int:team_id>/members', methods=['GET'])
def get_members(team_id):
    t = Team.query.get(team_id)
    if t is None:
        return {'errmsg': '此战队不存在', 'errcode': 404}, 404
    return {'members': t.get_members()}, 200


# 队员申请通过
@bp.route('/team/<int:team_id>/approve/<member_id>', methods=['PUT', 'POST'])
def approve_teammate(team_id, member_id):
    u = g.current_user
    t = Team.query.get(team_id)
    if t is None:
        return {'errmsg': '此战队不存在', 'errcode': 404}, 404
    if t.user_id != u.id:
        return {'errmsg': '没有权限', 'errcode': 403}, 403
    m = Member.query.get(member_id)
    if m is None:
        return {'errmsg': '此队员不存在', 'errcode': 404}, 404
    if m.team_id != t.id:
        return {'errmsg': '此队员不属于该战队', 'errcode': 403}, 403
    if m.approved == 1:
        return {'errmsg': '请勿重复通过申请', 'errcode': 403}, 403
    num = t.members.filter_by(approved=1).count()
    if t.num <= num:
        return {'errmsg': '小队人数已满', 'errcode': 403}, 403
    try:
        m.approved = 1
        db.session.commit()
    except:
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '通过成功', 'errcode': 200}, 200


@bp.route('/team/<int:team_id>/register', methods=['PUT', 'POST'])
def register_team(team_id):
    u = g.current_user
    t = Team.query.get(team_id)
    if t is None:
        return {'errmsg': '此战队不存在', 'errcode': 404}, 404
    if t.user_id != u.id:
        return {'errmsg': '没有权限', 'errcode': 403}, 403
    if t.success == 1:
        return {'errmsg': '请勿重复报名', 'errcode': 403}, 403
    num = t.members.filter_by(approved=1).count()
    if t.competition.min_num > num:
        return {'errmsg': '报名人数小于比赛要求', 'errcode': 403}, 403
    if datetime.now() > t.competition.apply_end:
        return {'errmsg': '比赛报名阶段已结束', 'errcode': 403}, 403
    try:
        for m in t.members.filter_by(approved=0).all():
            db.session.delete(m)
        t.success = 1
        db.session.commit()
    except:
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '报名成功', 'errcode': 200}, 200


@bp.route('/team/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    u = g.current_user
    t = Team.query.get(team_id)
    if t is None:
        return {'errmsg': '此战队不存在', 'errcode': 404}, 404
    if t.user_id != u.id:
        return {'errmsg': '没有权限', 'errcode': 403}, 403
    try:
        # for m in t.members.all():
        #     db.session.delete(m)
        db.session.delete(t)
        db.session.commit()
    except:
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '删除成功', 'errcode': 200}, 200

@bp.route('/team/<int:team_id>/member/<int:member_id>', methods=['DELETE'])
def delete_teamate(team_id,member_id):
    u = g.current_user
    t = Team.query.get(team_id)
    if t is None:
        return {'errmsg': '此战队不存在', 'errcode': 404}, 404
    if t.user_id != u.id:
        return {'errmsg': '没有权限', 'errcode': 403}, 403
    m = Member.query.get(member_id)
    if m is None:
        return {'errmsg': '此队员不存在', 'errcode': 404}, 404
    if m.team_id != t.id:
        return {'errmsg': '此队员不属于该战队', 'errcode': 403}, 403
    if t.success == 1:
        return {'errmsg': '已报名的小队无法修改', 'errcode': 403}, 403
    if m.user_id == t.user_id:
        return {'errmsg': '无法删除队长', 'errcode': 403}, 403
    try:
        db.session.delete(m)
        db.session.commit()
    except:
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '删除成功', 'errcode': 200}, 200