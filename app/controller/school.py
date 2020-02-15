# coding:utf-8
from . import bp
from app.models.school import School


@bp.route('/schools')
def get_schools():
    schools = School.query.all()
    return {
        'items': [val.to_dict() for val in schools],
        'errcode': 200
    }, 200
