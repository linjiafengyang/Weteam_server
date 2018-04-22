from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy();


class User(db.Model):
    """用户信息表"""
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    is_teacher = db.Column(db.Boolean, nullable=False)
    # 存 dict 形如 id1 : 0, id2 :0
    attended_course_id = db.Column(db.PickleType, nullable=True)
    username = db.Column(db.String(20), nullable=False)

    def __init__(self, student_id, name, is_teacher):
        self.student_id = student_id
        self.username = name
        self.is_teacher = is_teacher

    def add_user(self):
        """如果成功，那么就返回success，如果失败，返回失败原因"""
        if User.query.filter(self.student_id == User.student_id).first() is None:
            db.session.add(self)
            db.session.commit()
            return 'success'
        else:
            return 'already have this student_id'

    def delete_user(self):
        pass

    def __json__(self):
        info = {
            'user_id': self.user_id,
            'student_id': self.student_id,
            'username': self.username,
            'is_teacher': self.is_teacher,
            'attended_course_id': self.attended_course_id
        }
        return info


class Team(db.Model):
    """队伍表"""
    __tablename__ = 'teams'
    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    leader_id = db.Column(db.String(20), unique=True, nullable=False)
    team_info = db.Column(db.String(100), nullable=True)
    # list
    team_members_id = db.Column(db.PickleType, nullable=True)
    max_team = db.Column(db.Integer, nullable=False)
    available_team = db.Column(db.Integer, nullable=False)

    def __init__(self, leader_id, team_info, max_team):
        self.leader_id = leader_id
        self.team_info = team_info
        self.team_members_id = ''
        self.max_team = max_team
        self.available_team = max_team

    def __json__(self):
        info = {
            'team_id': self.team_id,
            'leader_id': self.leader_id,
            'team_info': self.team_info,
            'team_members_id': self.team_members_id,
            'max_team': self.max_team,
            'available_team': self.available_team
        }
        return info


class Course(db.Model):
    """课程表"""
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # list
    team_ids = db.Column(db.PickleType, nullable=True)
    course_info = db.Column(db.String(200), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    course_time = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    max_team = db.Column(db.Integer, nullable=False)
    min_team = db.Column(db.Integer, nullable=False)

    def __init__(self, course_info, name, course_time, start_time, end_time, max_team, min_team):
        self.course_info = course_info
        self.name = name
        self.course_time = course_time
        self.start_time = start_time
        self.end_time = end_time
        self.max_team = max_team
        self.min_team = min_team

    def __json__(self):
        info = {
            'course_id': self.course_id,
            'team_ids': self.team_ids,
            'course_info' : self.course_info,
            'name': self.name,
            'course_time': self.course_time,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'max_team': self.max_team,
            'min_team': self.min_team
        }