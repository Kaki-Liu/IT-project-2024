from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os
from schedule_generation import get_Schedule

# 初始化 Flask 应用
app = Flask(__name__, static_folder='../vit/dist')
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)


# 数据库模型
class Room(db.Model):
    __tablename__ = 'Room'
    RoomID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RoomName = db.Column(db.String(255), nullable=False)
    RoomType = db.Column(db.Integer, nullable=False)
    RoomCapacity = db.Column(db.Integer, nullable=False)
    RoomAddress = db.Column(db.String(255), nullable=False)
    CampusID = db.Column(db.Integer, nullable=False)
    RoomAvailableTimeStart = db.Column(db.SmallInteger, nullable=False)
    RoomAvailableTimeEnd = db.Column(db.SmallInteger, nullable=False)
    RoomAvailableDays = db.Column(db.SmallInteger, nullable=False)



class CourseTask(db.Model):
    __tablename__ = 'CourseTask'

    CourseTaskID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CourseTaskType = db.Column(db.Integer, nullable=False)
    TimePerWeek = db.Column(db.Integer, nullable=False)
    CoherenceRequirement = db.Column(db.Boolean, nullable=False)
    TeacherID = db.Column(db.Integer)
    CourseID = db.Column(db.Integer, nullable=False)
    RoomType = db.Column(db.Integer)
    CampusID = db.Column(db.Integer)

class NewSchedule(db.Model):
    __tablename__ = 'NewSchedule'
    SchemeID = db.Column(db.Integer, primary_key=True)
    Day = db.Column(db.String(50), nullable=False)
    StartTime = db.Column(db.String(50), nullable=False)
    EndTime = db.Column(db.String(50), nullable=False)
    CourseName = db.Column(db.String(255), nullable=False)
    RoomName = db.Column(db.String(255), nullable=False)
    RoomAddress = db.Column(db.String(255), nullable=False)
    CampusID = db.Column(db.Integer, nullable=False)
    RoomID = db.Column(db.Integer, primary_key=False)



# 根路径: 返回首页
@app.route('/', methods=['GET'])
def serve_home():
    return send_from_directory(app.static_folder, 'index.html')


# Classroom Management 页面路径和获取教室信息
@app.route('/classroom-management', methods=['GET', 'POST'])
def serve_classroom_management():
    print("查询中")
    if request.method == 'GET':
        if request.headers.get('Accept') == 'application/json':
            print("收到的 Campus ID:", request.args.get('campusId'))
            campus_id = request.args.get('campusId', type=int)
            if campus_id is not None:
                classrooms = Room.query.filter_by(CampusID=campus_id).all()
            else:
                classrooms = Room.query.all()
            result = [{
                'RoomID': classroom.RoomID,
                'RoomName': classroom.RoomName,
                'RoomType': classroom.RoomType,
                'RoomCapacity': classroom.RoomCapacity,
                'RoomAddress': classroom.RoomAddress,
                'CampusID': classroom.CampusID,
                'RoomAvailableTimeStart': classroom.RoomAvailableTimeStart,
                'RoomAvailableTimeEnd': classroom.RoomAvailableTimeEnd,
                'RoomAvailableDays': classroom.RoomAvailableDays
            } for classroom in classrooms]
            return jsonify(result)

        # 默认返回页面
        return send_from_directory(app.static_folder, 'index.html')

    elif request.method == 'POST':
        print("添加中11")
        try:
            data = request.get_json()
            print("接收到的数据:", data)

            new_room = Room(
                RoomName=data['RoomName'],
                RoomType=data['RoomType'],
                RoomCapacity=data['RoomCapacity'],
                RoomAddress=data['RoomAddress'],
                CampusID=data['CampusID'],
                RoomAvailableTimeStart=data['RoomAvailableTimeStart'],
                RoomAvailableTimeEnd=data['RoomAvailableTimeEnd'],
                RoomAvailableDays=data['RoomAvailableDays']
            )
            print("准备插入的新教室对象:", new_room)

            db.session.add(new_room)
            db.session.commit()
            print("教室添加成功")
            return jsonify({'message': 'Classroom added successfully!'}), 201
        except Exception as e:
            print("数据库提交失败，错误信息:", e)
            return jsonify({'message': f'Failed to add classroom: {str(e)}'}), 500


# 根据教室 ID 删除教室
@app.route('/classroom-management/<int:room_id>', methods=['DELETE'])
def delete_classroom(room_id):
    print(room_id)

    try:
        classroom = Room.query.get(room_id)
        if classroom is None:
            return jsonify({'message': 'Classroom not found'}), 404
        db.session.delete(classroom)
        db.session.commit()
        return jsonify({'message': 'Classroom deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Failed to delete classroom: {str(e)}'}), 500


@app.route('/course-management', methods=['GET', 'POST'])
def serve_course_management():
    print("查询课程任务中")
    if request.method == 'GET':
        print("Received GET request")
        print(request.args.get('campusId'))
        # 无论 Accept 头是否为 application/json，只要带有查询参数，返回 JSON 数据
        if request.args.get('campusId'):
            print("收到的 Campus ID:", request.args.get('campusId'))
            campus_id = request.args.get('campusId', type=int)
            if campus_id is not None:
                # 根据 CampusID 过滤课程任务
                print("not null")
                course_tasks = CourseTask.query.filter_by(CampusID=campus_id).all()
                print(course_tasks)
            else:
                # 如果没有提供 CampusID，则获取所有课程任务
                course_tasks = CourseTask.query.all()

            # 将查询结果转换为 JSON 格式返回
            result = [{
                'CourseTaskID': course_task.CourseTaskID,
                'CourseTaskType': course_task.CourseTaskType,
                'TimePerWeek': course_task.TimePerWeek,
                'CoherenceRequirement': course_task.CoherenceRequirement,
                'TeacherID': course_task.TeacherID,
                'CourseID': course_task.CourseID,
                'RoomType': course_task.RoomType,
                'CampusID': course_task.CampusID
            } for course_task in course_tasks]
            print(result)
            return jsonify(result)

        # 默认返回静态页面
        return send_from_directory(app.static_folder, 'index.html')

    elif request.method == 'POST':
        print("添加课程任务中")
        try:
            data = request.get_json()
            print("接收到的数据:", data)

            # 创建新的课程任务对象，并包括 CampusID
            new_course_task = CourseTask(
                CourseTaskType=data['courseTaskType'],
                TimePerWeek=data['timePerWeek'],
                CoherenceRequirement=data['coherenceRequirement'],
                TeacherID=data.get('teacherId'),
                CourseID=data['courseId'],
                RoomType=data.get('roomType'),
                CampusID=data.get('campusId')  # 添加 CampusID
            )
            print("准备插入的新课程任务对象:", new_course_task)

            # 将新任务添加到数据库并提交
            db.session.add(new_course_task)
            db.session.commit()
            print("课程任务添加成功")

            return jsonify({'message': 'Course task added successfully!'}), 201
        except Exception as e:
            print("数据库提交失败，错误信息:", e)
            return jsonify({'message': f'Failed to add course task: {str(e)}'}), 500




# Modify the original '/admin-timetable' endpoint to handle only campus ID requests
@app.route('/admin-timetable', methods=['GET', 'POST'])
def serve_admin_timetable():
    if request.method == 'POST':
        # Get campus ID from the request body
        data = request.get_json()
        campus_id = data.get('campusId')

        if campus_id is not None:
            print(f"Campus ID: {campus_id}")

            # Retrieve all rooms for the specified CampusID from Room table
            classrooms = Room.query.filter_by(CampusID=campus_id).all()

            # Create a response with room information
            rooms_data = [
                {
                    'RoomID': classroom.RoomID,
                    'RoomName': classroom.RoomName,
                    'RoomAddress': classroom.RoomAddress
                } for classroom in classrooms
            ]

            return jsonify({'message': f'Campus ID {campus_id} received successfully.', 'rooms': rooms_data}), 200
        else:
            return jsonify({'error': 'Campus ID not provided'}), 400

    # For GET requests, return the index.html file
    return send_from_directory(app.static_folder, 'index.html')

# Create a new endpoint to handle room-specific requests
@app.route('/admin-timetable/room', methods=['POST'])
def serve_room_timetable():
    # Get room ID from the request body
    data = request.get_json()
    room_id = data.get('roomId')

    if room_id is not None:
        print(f"Room ID: {room_id}")

        # Query the NewSchedule table for the room's schedule
        schedule_result = db.session.query(
            NewSchedule.Day,
            NewSchedule.StartTime,
            NewSchedule.EndTime,
            NewSchedule.CourseName
        ).filter(NewSchedule.RoomID == room_id).all()

        # Create a response with the schedule information
        schedule_data = [
            {
                'Day': item.Day,
                'StartTime': item.StartTime,
                'EndTime': item.EndTime,
                'CourseName': item.CourseName
            } for item in schedule_result
        ]
        print(schedule_data)

        return jsonify({'message': f'Room ID {room_id} received successfully.', 'schedule': schedule_data}), 200
    else:
        return jsonify({'error': 'Room ID not provided'}), 400


@app.route('/schedule-management', methods=['GET'])
def serve_schedule_generation():
    campus_id = request.args.get('campusId', type=int)
    if campus_id is None:
        return jsonify({'error': 'Campus ID is required'}), 400

    # Call the schedule generation function
    schedule_result = get_Schedule(campus_id)

    # Return success message to the front-end
    return jsonify({'message': schedule_result}), 200

# 静态文件服务
@app.route('/<path:path>', methods=['GET'])
def serve_vue(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/test-db', methods=['GET'])
def test_db_connection():
    try:
        test_query = Room.query.first()
        if test_query:
            return "数据库连接成功，能够查询到记录", 200
        else:
            return "数据库连接成功，但没有记录", 200
    except Exception as e:
        return f"数据库连接失败，错误信息: {e}", 500

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("数据库连接成功，所有表已创建")
        except Exception as e:
            print(f"数据库连接失败，错误信息: {e}")
    app.run(host='0.0.0.0', port=5002)





