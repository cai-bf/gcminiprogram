# coding:utf-8
from app import create_app, db
from app.models.user import User
from app.models.school import School
from app.models.competition import Competition
from app.models.team import Team
from app.models.member import Member
from app.models.message import Message
from app.models.read import Read


app = create_app()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=10000)
