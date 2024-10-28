from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CourseTask(db.Model):
    __tablename__ = 'course_tasks'
    id = db.Column(db.Integer, primary_key=True)
    task_type = db.Column(db.Integer, nullable=False)
    time_per_week = db.Column(db.Integer, nullable=False)
    coherence_requirement = db.Column(db.Boolean, nullable=False)
    teacher_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    room_type = db.Column(db.Integer, nullable=False)

class Classroom(db.Model):
    __tablename__ = 'classrooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    room_type = db.Column(db.Integer, nullable=False)  # 0 for Classroom, 1 for Lab
    number = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    available_time_start = db.Column(db.Integer, nullable=False)
    available_time_end = db.Column(db.Integer, nullable=False)
    available_days = db.Column(db.Integer, nullable=False)
    campus_id = db.Column(db.Integer, nullable=False)

