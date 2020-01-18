# coding:utf-8
from app import db
from . import bp
from app.models.message import Message
from flask import request, g, current_app, Response
from cerberus import Validator
from json import dumps
from app.models.read import Read
import xlwt
from io import BytesIO
import mimetypes


V = Validator()
V.allow_unknown = True


@bp.route('/messages', methods=['POST'])
def create_message():
    user = g.current_user
    if user.identify == 0:
        return {'errmsg': '没有权限发布通知', 'errcode': 403}, 403
    data = request.get_json()
    schema = {
        'title': {'type': 'string'},
        'content': {'type': 'string'},
        'pic': {'type': 'list', 'required': False}
    }
    if V.validate(data, schema) is False:
        return {'errmsg': '参数出错，请重新检查', 'errcode': 400}, 400
    images = data['pic'] if data.get('pic') is not None else []
    images = list(map(lambda x: current_app.config['IMG_BASE_URL'] + x, images))
    try:
        msg = Message(title=data['title'], content=data['content'], pic=dumps(images), user=user)
        db.session.add(msg)
        db.session.commit()
    except:
        return {'errmsg': '出现错误，请稍后再试～', 'errcode': 500}, 500
    return {'errmsg': '发布消息成功', 'errcode': 200}, 200


# 辅导员接口
@bp.route('/my_messages')
def get_my_messages():
    user = g.current_user
    if user.identify == 0:
        return {'errmsg': '没有权限查看', 'errcode': 403}, 403
    page = request.args.get('page', 1, type=int)
    msg = user.get_messages(page)
    return {
        'items': [val.to_dict() for val in msg.items],
        'has_next': msg.has_next,
        'has_prev': msg.has_prev,
        'page': msg.page,
        'pages': msg.pages,
        'per_page': msg.per_page,
        'prev_num': msg.prev_num,
        'next_num': msg.next_num,
        'total': msg.total
    }, 200


# 学生接口
@bp.route('/messages')
def get_messages():
    user = g.current_user
    if user.identify == 1:
        return {'errmsg': '教师辅导员无该数据', 'errcode': 403}, 403
    page = request.args.get('page', 1, type=int)
    teacher = user.teacher.first()
    msg = teacher.get_messages(page)
    return {
        'items': [val.to_dict(user.id) for val in msg.items],
        'has_next': msg.has_next,
        'has_prev': msg.has_prev,
        'page': msg.page,
        'pages': msg.pages,
        'per_page': msg.per_page,
        'prev_num': msg.prev_num,
        'next_num': msg.next_num,
        'total': msg.total
    }, 200


@bp.route('/messages/<int:msg_id>/read')
def read(msg_id):
    user = g.current_user
    msg = Message.query.get(msg_id)
    teacher = msg.user

    if user.identify != 0 or user.teacher.first().id != teacher.id:
        return {'errmsg': '没有权限', 'errcode': 403}, 403

    is_read = Read.query.filter_by(message_id=msg.id, user_id=user.id).first()
    if is_read:
        return {'errmsg': '已确认阅读，无需重复确认', 'errcode': 409}, 409

    r = Read(user_id=user.id, message_id=msg.id)
    db.session.add(r)
    Message.query.filter_by(id=msg_id).update({'read': Message.read + 1})
    db.session.commit()
    return {'errmsg': '已阅', 'errcode': 200}, 200


@bp.route('/export_read')
def export():
    msg_id = request.args.get('id')
    if msg_id is None:
        return {'errmsg': '参数缺失', 'errcode': 400}, 400
    user = g.current_user
    msg = Message.query.filter_by(id=msg_id).first()
    if msg is None:
        return {'errmsg': '无法完成请求', 'errcode': 406}, 406
    if msg.user_id != user.id:
        return {'errmsg': '没有权限', 'errcode': 403}, 403
    # generate excel
    f = xlwt.Workbook()
    sheet = f.add_sheet('学生已阅情况', True)
    sheet.write_merge(0, 0, 0, 4, msg.title)
    sheet.write(1, 0, '姓名')
    sheet.write(1, 1, '学号')
    sheet.write(1, 2, '是否已阅')
    i = 2
    for stu in user.students.all():
        sheet.write(i, 0, stu.name)
        sheet.write(i, 1, stu.number)
        sheet.write(i, 2, '是' if msg.reads.filter_by(user_id=stu.id) is not None else '')
        i += 1
    output = BytesIO()
    f.save(output)

    response = Response()
    response.status_code = 200
    response.data = output.getvalue()
    filename = 'read_statistic.xls'
    mime_tuple = mimetypes.guess_type(filename)
    response.headers['Content-Type'] = mime_tuple[0]
    response.headers['Content-Disposition'] = 'attachment; filename=\"%s\";' % filename
    if mime_tuple[1] is not None:
        response.headers['Content-Encoding'] = mime_tuple[1]
    return response
