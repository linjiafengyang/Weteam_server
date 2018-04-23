# coding:utf-8
from flask import Flask, request
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./Weteam.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# User部分


@app.route('/add_user', methods=['POST'])
def add_user():
    """使用于Post方法，用于向数据库中增加用户"""
    student_id = request.values.get('student_id')
    username = request.values.get('username')
    is_teacher = request.values.get('is_teacher')
    attended_course_ids = request.values.get('attended_course_ids')
    if attended_course_ids == 'None':
        attended_course_ids = None
    u = User(student_id, username, is_teacher, attended_course_ids)
    error = u.add_user()
    return error


@app.route('/get_user', methods=['GET'])
def get_user():
    student_id = request.values.get('student_id')
    u = User.query.filter(User.student_id == student_id).first()
    if u is None:
        return "400 : Cannot find such a student"
    else:
        return "200 : %s" % u.__json__()


@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    pass


@app.route('/modify_attended_course', methods=['POST'])
def modify_attended_course():
    """更改用户加入或创建的课程信息"""
    student_id = request.values.get('student_id')
    attended_course_ids = request.values.get('attended_course_ids')
    u = User.query.filter(User.student_id == student_id).first()
    if u is None:
        return "400 : Cannot find such a student"
    else:
        attended_course_ids = attended_course_ids.split('@')
        u.attended_course_ids = attended_course_ids
        db.session.add(u)
        db.session.commit()
        return "200 : success"

# Team部分


@app.route('/add_team', methods=['POST'])
def add_team():
    """向数据库中增加队伍"""
    course_id = request.values.get('course_id')
    leader_sid = request.values.get('leader_sid')
    team_info = request.values.get('team_info')
    max_team = request.values.get('max_team')
    available_team = request.values.get('available_team')
    team_members_id = request.values.get('team_members_id')
    team = Team(course_id, leader_sid, team_info, max_team, available_team, team_members_id)
    if Team.query.filter((team.course_id == Team.course_id) &
                         (team.leader_sid == Team.leader_sid)).first() is None:
        db.session.add(team)
        db.session.commit()
        return "200 : success"
    else:
        return "400 : Already have a team with this leader"


@app.route('/get_team', methods=['GET'])
def get_team():
    """获取队伍信息"""
    team_id = request.values.get('team_id')
    team = Team.query.filter(team_id == Team.team_id).first()
    if team is None:
        return "400 : Cannot find such a team"
    else:
        return "200 : %s" % team.__json__()


@app.route('/delete_team', methods=['DELETE'])
def delete_team():
    """删除队伍"""
    team_id = request.values.get('team_id')
    team = Team.query.filter(team_id == Team.team_id).first()
    if team is None:
        return "400 : Cannot find such a team"
    else:
        db.session.delete(team)
        db.session.commit()
        return "200 : success"


@app.route('/modify_team', methods=['POST'])
def modify_team():
    team_id = request.values.get('team_id')
    team_members_id = request.values.get('team_members_id')
    team = Team.query.filter(team_id == Team.team_id).first()
    if team is None:
        return "400 : Cannot find such a team"
    else:
        team_members_id = team_members_id.split('@')
        team.team_members_id = team_members_id
        db.session.add(team)
        db.session.commit()
        return "200 : success"

# Course部分


@app.route('/add_course', methods=['POST'])
def add_course():
    teacher_id = request.values.get('teacher_id')
    team_ids = request.values.get('team_ids')
    student_ids = request.values.get('student_ids')
    course_info = request.values.get('course_info')
    name = request.values.get('name')
    course_time = request.values.get('course_time')
    start_time = request.values.get('start_time')
    end_time = request.values.get('end_time')
    max_team = request.values.get('max_team')
    min_team = request.values.get('min_team')
    course = Course(teacher_id, course_info, name, course_time, start_time,
                    end_time, max_team, min_team, student_ids, team_ids)
    if Course.query.filter((course.teacher_id == Course.teacher_id)
                           & (name == Course.name) &
                           (course_time == Course.course_time)).first() is None:
        db.session.add(course)
        db.session.commit()
        return '200 : success'
    else:
        return '400 : Already have this class'


@app.route('/get_course', methods=['GET'])
def get_course():
    course_id = request.values.get('course_id')
    course = Course.query.filter(course_id == Course.course_id).first()
    if course is None:
        return '400 : Cannot find this course'
    else:
        return '200 : %s' % course.__json__();


@app.route('/delete_course', methods=['POST'])
def delete_course():
    course_id = request.values.get('course_id')
    course = Course.query.filter(course_id == Course.course_id).first()
    if course is None:
        return '400 : Cannot find this course'
    else:
        db.session.delete(course)
        db.session.commit()
        return '200 : success'


@app.route('/course_modify_team', methods=['POST'])
def course_modify_team():
    """增删队伍"""
    course_id = request.values.get('course_id')
    team_ids = request.values.get('team_ids')
    course = Course.query.filter(course_id == Course.course_id).first()
    if course is None:
        return '400 : Cannot find such a course'
    else:
        team_ids = team_ids.split('@')
        course.team_ids = team_ids
        db.session.add(course)
        db.session.commit()
        return '200 : success'


@app.route('/course_modify_student', methods=['POST'])
def course_modify_student():
    """对于课程增删学生"""
    course_id = request.values.get('course_id')
    student_ids = request.values.get('student_ids')
    course = Course.query.filter(course_id == Course.course_id).first()
    if course is None:
        return '400 : Cannot find such a course'
    else:
        temp = student_ids.split('@')
        student_ids = {}
        for a in temp:
            p = a.split(':')
            student_ids[p[0]] = p[1]
        course.student_ids = student_ids
        db.session.add(course)
        db.session.commit()
        return '200 : success'


if __name__ == '__main__':
    db.app = app
    db.init_app(app)
    db.create_all()
    app.run(host='0.0.0.0', debug=True, port=3000)
