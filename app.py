# coding:utf-8
from flask import Flask
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


@app.route('/add/<student_id>/<name>/<is_teacher>')
def add(student_id, name, is_teacher):
    u = User(student_id, name, is_teacher)
    u.add_user()
    return "hello %s" % u.__json__()


@app.route('/get/<student_id>')
def get(student_id):
    try:
        u = User.query.filter(User.student_id == student_id).first()
    except(Exception, e):
        return 'there is not %s' % student_id
    return 'hello %s' % u.__json__()


if __name__ == '__main__':
    db.app = app
    db.init_app(app)
    db.create_all()
    app.run(debug=True, port=3000);
