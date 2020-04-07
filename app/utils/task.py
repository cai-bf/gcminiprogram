# coding:utf-8
from app import create_app
from app.models import user
from wechatpy import WeChatClient
from config import Config
from app.models.message import Message

app = create_app(Config)
app.app_context().push()


def send_template(teacher_id, msg_id):
    wx = WeChatClient(app.config['APP_ID'], app.config['APP_SECRET'],
                      session=app.wx_session)
    msg = Message.query.get(msg_id)
    teacher = user.check_user_by_id(teacher_id)
    for stu in teacher.students.all():
        wx.message.send_template(stu.follower.openid, app.config['MSG_TEMPLATE_ID'],  {
            "first": {
                "value": stu.name + '同学, 你有一条新的通知',
                "color": '#8c8c8c'
            },
            "keyword1": {
                "value": msg.title,
                "color": '#173177'
            },
            "keyword2": {
                "value": msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "color": '#173177'
            },
            "keyword3": {
                "value": '点击进入小程序查看详细内容',
                "color": '#173177'
            }
        }, mini_program={
            "appid": app.config['APP_MINI_ID'],
            "pagepath": 'pages/student/detail/detail'
        })
