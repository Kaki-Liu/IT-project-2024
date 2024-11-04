from random import randint

from ortools.sat.python import cp_model
import json
import psycopg2

RoomTypes = {
    0: "classroom",
    1: "lab"
}

CouseTypes = {
    0: "讲座",
    1: "训练",
    2: "试验",
    3: "实践"
}

# 星期映射表
weekdays = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday"
}

campuses = {
    0: "Melbourne",
    1: "Geelong",
    2: "Sydney",
    3: "Adelaide"
}

def int_to_bit_positions(n):
    positions = []
    bit_position = 0
    while n > 0:
        if n & 1 == 1:  # 检查当前位是否为1
            positions.append(bit_position)
        n >>= 1  # 右移一位
        bit_position += 1
    return positions

def SQLExe(sql, cur):
    #print(sql)
    cur.execute(sql)
    r = cur.fetchall()  # 取数据
    return r

def get_Schedule(CampusID):
    """
    # 读取输入数据
    with open('input.json', 'r') as f:
        data = json.load(f)

    courses = data['courses']
    classrooms = data['classrooms']
    students = data['students']
    teachers = data['teachers']
    """

    Semester = 0  # 学期
    SchemeID = 0 #排课方案序号号，每次排课方案号不同，用于便捷区分多次排课的结果

    # 链接数据库
    import psycopg2

    conn = psycopg2.connect(
        database='IT_database',
        user='postgres',
        password='',
        host='localhost',  # 改为 'localhost' 或 '127.0.0.1'
        port='5432'  # 改为 PostgreSQL 实际运行的端口，默认是 '5432'
    )
    cur = conn.cursor()
    cur.execute('TRUNCATE TABLE "public"."Schedule";')
    conn.commit()  # Commit the changes



    # 获取有人选的课程数据
    sql = (
            'SELECT DISTINCT "CourseTask"."CourseTaskID", "Course"."CourseName", "CourseTask"."CourseTaskType", \
            "CourseTask"."TeacherID", "CourseTask"."TimePerWeek", "CourseTask"."RoomType" \
            FROM "public"."Course", "public"."CourseTask", "public"."CourseSel" \
            WHERE "CourseSel"."CourseID" = "Course"."CourseID" AND "CourseTask"."CourseID" = "Course"."CourseID" \
            AND "Course"."Semester" = "CourseSel"."Semester" AND "Course"."CampusID" = "CourseSel"."CampusID"\
            AND "TimePerWeek" > 0 AND "Course"."Semester" = %d AND "Course"."CampusID" = %d;' % (Semester, CampusID))
    rows = SQLExe(sql, cur)
    courses = []
    for row in rows:
        r = {"id": row[0], "name": row[1] + '(' + CouseTypes[row[2]] + ")",
             "teacherId": row[3], "weeklyHours": row[4], "roomType": RoomTypes[row[5]]}
        courses.append(r)
    print(courses)

    # 获取所有教室数据
    sql = ('SELECT * FROM "public"."Room" WHERE "Room"."CampusID" = %d;' % (CampusID))
    rows = SQLExe(sql, cur)
    classrooms = []
    for row in rows:
        openday = int_to_bit_positions(row[8])
        r = {"id": row[0], "name": row[1], "capacity": row[3], "opentime": row[6],
             "closetime": row[7], "openday": openday, "type": RoomTypes[row[2]]}
        classrooms.append(r)

    # 获取学生基本信息
    sql = ('SELECT * FROM "public"."Student" WHERE "CampusID" = %d and "StudentValid" = TRUE;' % (CampusID))
    rows = SQLExe(sql, cur)
    students = []
    for row in rows:
        r = {"id": row[0], "name": row[3], "courseIds": []}
        students.append(r)

    # 获取每个学生的选课数据
    for s in students:
        sql = ('SELECT "CourseTaskID" \
        FROM "public"."CourseSel", "public"."CourseTask" \
        WHERE "CourseTask"."CourseID" = "CourseSel"."CourseID" \
        AND "TimePerWeek" > 0 \
        AND "StudentID" = %d AND "Semester" = %d AND  "CourseSel"."CampusID" = %d;' % (s['id'], Semester, CampusID))
        rows = SQLExe(sql, cur)
        for row in rows:
            s["courseIds"].append(row[0])
    print(students)

    # 在被人选的需要上课的子课程中获取分配老师的数据
    sql = ('SELECT DISTINCT "Teacher"."TeacherID", "Teacher"."TeacherName" \
     FROM "public"."Teacher", "public"."CourseTask", "public"."CourseSel" \
     WHERE "Teacher"."TeacherID" = "CourseTask"."TeacherID" AND "CourseSel"."CourseID" = "CourseTask"."CourseID" \
     AND "CourseTask"."TimePerWeek" > 0 \
     AND "CourseSel"."Semester" = %d AND "CourseSel"."CampusID" = %d;' % (Semester, CampusID))
    rows = SQLExe(sql, cur)
    teachers = []
    for row in rows:
        r = {"id": row[0], "name": row[1]}
        teachers.append(r)
    print(teachers)
    # 创建CSP模型
    model = cp_model.CpModel()

    # 获取所有可能的时间段和教室组合
    time_slots = []
    for r in classrooms:
        for d in r['openday']:
            for h in range(r['opentime'], r['closetime']):
                time_slots.append((r['id'], d, h))

    # 为每个课程创建可能的排课时段变量
    schedule = {}
    for c in courses:
        for r in classrooms:
            if r['type'] == c['roomType']:
                for d in r['openday']:
                    for h in range(r['opentime'], r['closetime']):
                        schedule[(c['id'], r['id'], d, h)] = model.NewBoolVar(
                            f'schedule_c{c["id"]}_r{r["id"]}_d{d}_h{h}')

    # 为每个学生创建选课变量
    student_attend = {}
    for s in students:
        for c in courses:
            if c['id'] in s['courseIds']:
                for r in classrooms:
                    if r['type'] == c['roomType']:
                        for d in r['openday']:
                            for h in range(r['opentime'], r['closetime']):
                                student_attend[(s['id'], c['id'], r['id'], d, h)] = model.NewBoolVar(
                                    f'student_s{s["id"]}_c{c["id"]}_r{r["id"]}_d{d}_h{h}')

    # 为每个课程计算需要的最少分组数以满足教室容量限制
    course_students = {}
    for c in courses:
        enrolled_students = [s for s in students if c['id'] in s['courseIds']]
        course_students[c['id']] = enrolled_students

    # 约束1：课程必须在开放的时段和教室内安排
    for c in courses:
        total_hours = c['weeklyHours']
        possible_slots = [key for key in schedule if key[0] == c['id']]
        model.Add(
            sum(schedule[key] for key in possible_slots) == total_hours
        )

    # 约束2：教室同一时间只能安排一个课程
    for r in classrooms:
        for d in r['openday']:
            for h in range(r['opentime'], r['closetime']):
                model.Add(
                    sum(
                        schedule[(c['id'], r['id'], d, h)]
                        for c in courses
                        if (c['id'], r['id'], d, h) in schedule
                    ) <= 1
                )

    # 约束3：教师同一时间只能上一个课程和一个教室
    for t in teachers:
        for d in range(1, 6):
            for h in range(8, 22):  # 假设所有教室的开放时间在8到22点之间
                model.Add(
                    sum(
                        schedule[(c['id'], r['id'], d, h)]
                        for c in courses if c['teacherId'] == t['id']
                        for r in classrooms if (c['id'], r['id'], d, h) in schedule
                    ) <= 1
                )

    # # 约束4：学生同一时间只能上一个课程和一个教室
    # for s in students:
    #     for d in range(1, 6):
    #         for h in range(8, 22):
    #             model.Add(
    #                 sum(
    #                     student_attend[(s['id'], c['id'], r['id'], d, h)]
    #                     for c in courses if c['id'] in s['courseIds']
    #                     for r in classrooms if (s['id'], c['id'], r['id'], d, h) in student_attend
    #                 ) <= 1
    #             )
    #
    # # 约束5：如果学生在某时段上某课程，则该课程必须在该时段的该教室上课
    # for key in student_attend:
    #     s_id, c_id, r_id, d, h = key
    #     model.AddImplication(
    #         student_attend[key],
    #         schedule[(c_id, r_id, d, h)]
    #     )

    # 约束6：教室容量限制
    for c in courses:
        for r in classrooms:
            if r['type'] == c['roomType']:
                for d in r['openday']:
                    for h in range(r['opentime'], r['closetime']):
                        student_keys = [
                            (s['id'], c['id'], r['id'], d, h)
                            for s in students if c['id'] in s['courseIds']
                            if (s['id'], c['id'], r['id'], d, h) in student_attend
                        ]
                        if student_keys:
                            model.Add(
                                sum(
                                    student_attend[key] for key in student_keys
                                ) <= r['capacity']
                            )

    # 约束7：每个学生必须完成每门课程的所有学时
    for s in students:
        for c in courses:
            if c['id'] in s['courseIds']:
                model.Add(
                    sum(
                        student_attend[(s['id'], c['id'], r['id'], d, h)]
                        for r in classrooms if r['type'] == c['roomType']
                        for d in r['openday']
                        for h in range(r['opentime'], r['closetime'])
                        if (s['id'], c['id'], r['id'], d, h) in student_attend
                    ) == c['weeklyHours']
                )

    # 约束8：学生只能在课程安排的时段上课
    for s in students:
        for c in courses:
            if c['id'] in s['courseIds']:
                for r in classrooms:
                    if r['type'] == c['roomType']:
                        for d in r['openday']:
                            for h in range(r['opentime'], r['closetime']):
                                if (s['id'], c['id'], r['id'], d, h) in student_attend and (
                                        c['id'], r['id'], d, h) in schedule:
                                    model.AddImplication(
                                        student_attend[(s['id'], c['id'], r['id'], d, h)],
                                        schedule[(c['id'], r['id'], d, h)]
                                    )

    # 求解模型
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # 输出结果
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("找到可行的解决方案：")

        #获取方案序号自增1，COALESCE:空表NULL时返回0
        sql = 'SELECT COALESCE(max("SchemeID"),0) FROM "public"."Schedule";'
        rows = SQLExe(sql, cur)
        SchemeID = rows[0][0] + 1#准备插入的数据

        # 打印课程安排
        print("\n课程安排：")
        for c in courses:
            print(f"课程 {c['name']} (ID: {c['id']}):")
            for r in classrooms:
                for d in r['openday']:
                    for h in range(r['opentime'], r['closetime']):
                        if (c['id'], r['id'], d, h) in schedule and solver.Value(schedule[(c['id'], r['id'], d, h)]):
                            teacher = next((t['name'] for t in teachers if t['id'] == c['teacherId']), 'Unknown')
                            print(f"  {weekdays[d]} 第{h}节课 在教室 {r['name']} 上课 (教师: {teacher})")

                            # 准备插入的数据
                            CourseTaskID = c['id'];
                            CourseTime = h;
                            CourseDay = d;
                            RoomID = r['id'];
                            sql_reset= ('TRUNCATE TABLE "public"."Schedule";')
                            #插入排课计划
                            sql = ('INSERT INTO "public"."Schedule" ("SchemeID", "CourseTaskID", "Day", "Time", "RoomID", "CampusID", "Semester") VALUES(%d, %d, %d, %d, %d, %d, %d);' % (SchemeID, CourseTaskID, CourseDay, CourseTime, RoomID, CampusID, Semester))
                            # cur.execute(sql_reset)
                            cur.execute(sql)
                            conn.commit()

                            students_in_class = [
                                s['name'] for s in students
                                if (s['id'], c['id'], r['id'], d, h) in student_attend and solver.Value(
                                    student_attend[(s['id'], c['id'], r['id'], d, h)])
                            ]
                            print(f"    学生: {', '.join(students_in_class)}")

        # # 打印教师课程表
        # print("\n教师课程表：")
        # for t in teachers:
        #     print(f"教师 {t['name']} (ID: {t['id']}):")
        #     for c in courses:
        #         if c['teacherId'] == t['id']:
        #             for r in classrooms:
        #                 for d in r['openday']:
        #                     for h in range(r['opentime'], r['closetime']):
        #                         if (c['id'], r['id'], d, h) in schedule and solver.Value(
        #                                 schedule[(c['id'], r['id'], d, h)]):
        #                             print(f"  {weekdays[d]} 第{h}节课 教 {c['name']} 在教室 {r['name']}")
        #
        # # 打印学生课程表
        # print("\n学生课程表：")
        # for s in students:
        #     print(f"学生 {s['name']} (ID: {s['id']}):")
        #     for c in courses:
        #         if c['id'] in s['courseIds']:
        #             for r in classrooms:
        #                 for d in r['openday']:
        #                     for h in range(r['opentime'], r['closetime']):
        #                         if (s['id'], c['id'], r['id'], d, h) in student_attend and solver.Value(
        #                                 student_attend[(s['id'], c['id'], r['id'], d, h)]):
        #                             teacher = next((t['name'] for t in teachers if t['id'] == c['teacherId']),
        #                                            'Unknown')
        #                             print(
        #                                 f"  {weekdays[d]} 第{h}节课 上 {c['name']} 在教室 {r['name']} (教师: {teacher})")

        #排课信息获取示例
        print('排课信息数据库查找示例')
        sql = ('SELECT "Course"."CourseName", "CourseTask"."CourseTaskType", "Teacher"."TeacherName", "Schedule"."Day", "Schedule"."Time", "CourseTask"."TimePerWeek", "Room"."RoomName", "Room"."RoomAddress" \
        FROM "public"."Schedule", "public"."CourseTask", "public"."Room", "public"."Course", "public"."Teacher" \
        WHERE "Schedule"."CourseTaskID" = "CourseTask"."CourseTaskID" AND "Schedule"."RoomID" = "Room"."RoomID" \
        AND "Course"."CourseID" = "CourseTask"."CourseID" AND "CourseTask"."TeacherID" = "Teacher"."TeacherID" \
        AND "Course"."CampusID" = %d AND "Course"."Semester" = %d AND "Schedule"."SchemeID" = %d;' % (CampusID, Semester, SchemeID))
        print(sql)
        rows = SQLExe(sql, cur)
        print('第%d号校区，第%d学期，第%d号排课方案:'%(CampusID, Semester, SchemeID))
        for row in rows:
            CourseSchedule = '课程：' + row[0] + '（' + CouseTypes[row[1]] + '）；教师：' + row[2] + '；每周' + weekdays[row[3]] + \
                            str(row[4]) + ':00至' + str(row[4] + row[5]) + ':00上课；教室名称：' + row[6] + '；教室地址：' + row[7]
            print(CourseSchedule)
        sql = ('DELETE FROM "public"."NewSchedule" WHERE "CampusID" = %d;  \
        INSERT INTO "public"."NewSchedule"\
        SELECT \
            sch."SchemeID",\
            sch."Day",\
            sch."Time" AS "StartTime",\
            (sch."Time" + ct."TimePerWeek") AS "EndTime",\
            c."CourseName",\
            r."RoomID",\
            r."RoomName",\
            r."RoomAddress",\
            sch."CampusID"\
        FROM \
            "public"."Schedule" sch\
        JOIN \
            "public"."CourseTask" ct ON sch."CourseTaskID" = ct."CourseTaskID"\
        JOIN \
            "public"."Course" c ON ct."CourseID" = c."CourseID"\
        JOIN \
            "public"."Room" r ON sch."RoomID" = r."RoomID"\
        WHERE \
            ct."TimePerWeek" > 0;'%CampusID)
        cur.execute(sql)
        conn.commit()

    else:
        print("未找到可行的解决方案。")

    conn.close()

if __name__ == "__main__":
    get_Schedule(0)