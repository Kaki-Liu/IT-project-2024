from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

# 初始化 Flask 应用
app = Flask(__name__, static_folder='../vit/dist')
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)

# 数据库模型
class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(100), nullable=False)
    classroom = db.Column(db.String(100), nullable=False)
    lecturer = db.Column(db.String(100), nullable=False)
    tutor = db.Column(db.String(100), nullable=False)
    delivery_mode = db.Column(db.String(100), nullable=False)

# 根路径: 返回首页
@app.route('/', methods=['GET'])
def serve_home():
    return send_from_directory(app.static_folder, 'index.html')

# API 首页
@app.route('/api/', methods=['GET'])
def api_home():
    return jsonify({'message': 'Welcome to the API'})

# 静态文件服务
@app.route('/<path:path>', methods=['GET'])
def serve_vue(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Classroom Management 路由
@app.route('/api/classrooms', methods=['POST'])
def add_classroom():
    data = request.get_json()
    new_classroom = Classroom(
        name=data['name'],
        number=data['number'],
        capacity=data['capacity']
    )
    db.session.add(new_classroom)
    db.session.commit()
    return jsonify({'message': 'Classroom added successfully!'}), 201

# 获取所有教室信息
@app.route('/api/classrooms', methods=['GET'])
def get_classrooms():
    classrooms = Classroom.query.all()
    result = [{
        'id': classroom.id,
        'name': classroom.name,
        'number': classroom.number,
        'capacity': classroom.capacity
    } for classroom in classrooms]
    return jsonify(result)

# Course Management 路由
@app.route('/api/courses', methods=['POST'])
def add_course():
    data = request.get_json()
    new_course = Course(
        date=data['date'],
        time=data['time'],
        unit=data['unit'],
        classroom=data['classroom'],
        lecturer=data['lecturer'],
        tutor=data['tutor'],
        delivery_mode=data['delivery_mode']
    )
    db.session.add(new_course)
    db.session.commit()
    return jsonify({'message': 'Course added successfully!'}), 201

# Admin Timetable 路由
@app.route('/api/timetable', methods=['GET'])
def get_timetable():
    courses = Course.query.all()
    timetable = [{
        'date': course.date,
        'time': course.time,
        'unit': course.unit,
        'classroom': course.classroom,
        'lecturer': course.lecturer,
        'tutor': course.tutor,
        'delivery_mode': course.delivery_mode
    } for course in courses]
    return jsonify(timetable)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002)
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

# 初始化 Flask 应用
app = Flask(__name__, static_folder='../vit/dist')
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)

# 数据库模型
class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(100), nullable=False)
    classroom = db.Column(db.String(100), nullable=False)
    lecturer = db.Column(db.String(100), nullable=False)
    tutor = db.Column(db.String(100), nullable=False)
    delivery_mode = db.Column(db.String(100), nullable=False)

# 根路径: 返回首页
@app.route('/', methods=['GET'])
def serve_home():
    return send_from_directory(app.static_folder, 'index.html')

# API 首页
@app.route('/api/', methods=['GET'])
def api_home():
    return jsonify({'message': 'Welcome to the API'})

# 静态文件服务
@app.route('/<path:path>', methods=['GET'])
def serve_vue(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Classroom Management 路由
@app.route('/api/classrooms', methods=['POST'])
def add_classroom():
    data = request.get_json()
    new_classroom = Classroom(
        name=data['name'],
        number=data['number'],
        capacity=data['capacity']
    )
    db.session.add(new_classroom)
    db.session.commit()
    return jsonify({'message': 'Classroom added successfully!'}), 201

# 获取所有教室信息
@app.route('/api/classrooms', methods=['GET'])
def get_classrooms():
    classrooms = Classroom.query.all()
    result = [{
        'id': classroom.id,
        'name': classroom.name,
        'number': classroom.number,
        'capacity': classroom.capacity
    } for classroom in classrooms]
    return jsonify(result)

# Course Management 路由
@app.route('/api/courses', methods=['POST'])
def add_course():
    data = request.get_json()
    new_course = Course(
        date=data['date'],
        time=data['time'],
        unit=data['unit'],
        classroom=data['classroom'],
        lecturer=data['lecturer'],
        tutor=data['tutor'],
        delivery_mode=data['delivery_mode']
    )
    db.session.add(new_course)
    db.session.commit()
    return jsonify({'message': 'Course added successfully!'}), 201

# Admin Timetable 路由
@app.route('/api/timetable', methods=['GET'])
def get_timetable():
    courses = Course.query.all()
    timetable = [{
        'date': course.date,
        'time': course.time,
        'unit': course.unit,
        'classroom': course.classroom,
        'lecturer': course.lecturer,
        'tutor': course.tutor,
        'delivery_mode': course.delivery_mode
    } for course in courses]
    return jsonify(timetable)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002)








