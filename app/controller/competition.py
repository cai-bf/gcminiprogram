# coding:utf-8
from . import bp
from flask import g, request, current_app
from app import db
from json import dumps
from app.models.competition import Competition
from cerberus import Validator
from datetime import datetime


class MyValidator(Validator):
    def _validate_time_after(self, other, field, value):
        if other not in self.document:
            return False
        if value < self.document[other]:
            self._error(field, "is earlier than %s." % other)

    def _validate_time_now(self, check, field, value):
        if check and value < datetime.now():
            self._error(field, "is earlier than now.")


def to_date(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


V = MyValidator()
V.allow_unknown = True


@bp.route('/competition', methods=['POST'])
def create_competition():
    u = g.current_user
    if u.identify == 0:
        return {'errmsg': '没有权限发布比赛', 'errcode': 403}, 403
    data = request.get_json()
    schema = {
        'title': {'type': 'string'},
        'min_num': {'type': 'integer'},
        'max_num': {'type': 'integer'},
        'apply_start': {'type': 'datetime', 'coerce': to_date, 'time_now': True},
        'apply_end': {'type': 'datetime', 'coerce': to_date, 'time_after': 'apply_start'},
        'start_time': {'type': 'datetime', 'coerce': to_date, 'time_now': True, 'time_after': 'apply_end'},
        'end_time': {'type': 'datetime', 'coerce': to_date, 'time_after': 'start_time'},
        'remark': {'type': 'string'},
        'poster': {'type': 'list'}
    }
    if V.validate(data, schema) is False:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    images = data['poster'] if data.get('poster') is not None else []
    images = list(map(lambda x: current_app.config['IMG_BASE_URL'] + x, images))
    try:
        c = Competition(
            user=u,
            title=data['title'],
            min_num=data['min_num'],
            max_num=data['max_num'],
            apply_start=data['apply_start'],
            apply_end=data['apply_end'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            remark=data['remark'],
            poster=dumps(images)
        )
        db.session.add(c)
        db.session.commit()
    except:
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '发布比赛成功', 'errcode': 200}, 200


@bp.route('/competitions', methods=['GET'])
def get_competitions():
    u = g.current_user
    my = request.args.get('my', False, type=bool)
    title = request.args.get('title')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    if my:
        c = u.competition.order_by(Competition.created_at.desc()).paginate(page, per_page, error_out=False)
    elif title is None:
        c = Competition.query.order_by(Competition.created_at.desc()).paginate(page, per_page, error_out=False)
    else:
        c = Competition.query.filter(Competition.title.like("%"+title+"%")).order_by(Competition.created_at.desc())\
            .paginate(page, per_page, error_out=False)
    return {
        'items': [val.to_dict() for val in c.items],
        'has_next': c.has_next,
        'has_prev': c.has_prev,
        'page': c.page,
        'pages': c.pages,
        'per_page': c.per_page,
        'prev_num': c.prev_num,
        'next_num': c.next_num,
        'total': c.total
    }, 200


@bp.route('/competition/<int:competition_id>', methods=['DELETE'])
def delete_competition(competition_id):
    u = g.current_user
    c = Competition.query.get(competition_id)
    if c is None:
        return {'errmsg': '此比赛不存在', 'errcode': 404}, 404
    if u != c.user:
        return {'errmsg': '非大赛创建者', 'errcode': 403}, 403
    try:
        db.session.delete(c)
        db.session.commit()
    except:
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '删除比赛成功', 'errcode': 200}, 200
