from random import randint

from ortools.sat.python import cp_model
import json
import psycopg2

RoomTypes = {
    0: "classroom",
    1: "lab"
}

CouseTypes = {
    0: "lecture",
    1: "training",
    2: "experiment",
    3: "practice"
}

# Weekday mapping table
weekdays = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday"
}

def int_to_bit_positions(n):
    positions = []
    bit_position = 0
    while n > 0:
        if n & 1 == 1:  # Check if the current bit is 1
            positions.append(bit_position)
        n >>= 1  # Right shift by one bit
        bit_position += 1
    return positions

def SQLExe(sql, cur):
    #print(sql)
    cur.execute(sql)
    r = cur.fetchall()  # Fetch data
    return r

def main():
    """
    # Read input data
    with open('input.json', 'r') as f:
        data = json.load(f)

    courses = data['courses']
    classrooms = data['classrooms']
    students = data['students']
    teachers = data['teachers']
    """

    Semester = 0  # Semester
    CampusID = 0  # Campus ID
    SchemeID = 0 # Course scheduling scheme number, different for each scheduling to conveniently distinguish results

    # Connect to database
    conn = psycopg2.connect(database='Course', user='postgres', password='', host='172.26.64.1', port='65432')
    cur = conn.cursor()

    # Get courses that have enrolled students
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

    # Get all classroom data
    sql = ('SELECT * FROM "public"."Room" WHERE "CampusID" = %d;' % (CampusID))
    rows = SQLExe(sql, cur)
    classrooms = []
    for row in rows:
        openday = int_to_bit_positions(row[8])
        r = {"id": row[0], "name": row[1], "capacity": row[3], "opentime": row[6],
             "closetime": row[7], "openday": openday, "type": RoomTypes[row[2]]}
        classrooms.append(r)

    # Get student basic information
    sql = ('SELECT * FROM "public"."Student" WHERE "CampusID" = %d and "StudentValid" = TRUE;' % (CampusID))
    rows = SQLExe(sql, cur)
    students = []
    for row in rows:
        r = {"id": row[0], "name": row[3], "courseIds": []}
        students.append(r)

    # Get each student's course selection data
    for s in students:
        sql = ('SELECT "CourseTaskID" \
        FROM "public"."CourseSel", "public"."CourseTask" \
        WHERE "CourseTask"."CourseID" = "CourseSel"."CourseID" \
        AND "TimePerWeek" > 0 \
        AND "StudentID" = %d AND "Semester" = %d AND "CampusID" = %d;' % (s['id'], Semester, CampusID))
        rows = SQLExe(sql, cur)
        for row in rows:
            s["courseIds"].append(row[0])

    # Get teacher data for assigned courses that have enrolled students
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
    # Create CSP model
    model = cp_model.CpModel()

    # Get all possible time slots and classroom combinations
    time_slots = []
    for r in classrooms:
        for d in r['openday']:
            for h in range(r['opentime'], r['closetime']):
                time_slots.append((r['id'], d, h))

    # Create possible scheduling time slot variables for each course
    schedule = {}
    for c in courses:
        for r in classrooms:
            if r['type'] == c['roomType']:
                for d in r['openday']:
                    for h in range(r['opentime'], r['closetime']):
                        schedule[(c['id'], r['id'], d, h)] = model.NewBoolVar(
                            f'schedule_c{c["id"]}_r{r["id"]}_d{d}_h{h}')

    # Create attendance variables for each student
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

    # Calculate the minimum number of groups required for each course to meet classroom capacity limits
    course_students = {}
    for c in courses:
        enrolled_students = [s for s in students if c['id'] in s['courseIds']]
        course_students[c['id']] = enrolled_students

    # Constraint 1: Courses must be scheduled in open time slots and classrooms
    for c in courses:
        total_hours = c['weeklyHours']
        possible_slots = [key for key in schedule if key[0] == c['id']]
        model.Add(
            sum(schedule[key] for key in possible_slots) == total_hours
        )

    # Constraint 2: A classroom can only be assigned one course at the same time
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

    # Constraint 3: A teacher can only teach one course in one classroom at the same time
    for t in teachers:
        for d in range(1, 6):
            for h in range(8, 22):  # Assume all classrooms are open from 8 AM to 10 PM
                model.Add(
                    sum(
                        schedule[(c['id'], r['id'], d, h)]
                        for c in courses if c['teacherId'] == t['id']
                        for r in classrooms if (c['id'], r['id'], d, h) in schedule
                    ) <= 1
                )

    # Constraint 4: A student can only attend one course in one classroom at the same time
    for s in students:
        for d in range(1, 6):
            for h in range(8, 22):
                model.Add(
                    sum(
                        student_attend[(s['id'], c['id'], r['id'], d, h)]
                        for c in courses if c['id'] in s['courseIds']
                        for r in classrooms if (s['id'], c['id'], r['id'], d, h) in student_attend
                    ) <= 1
                )

    # Constraint 5: If a student attends a course at a specific time, that course must be scheduled in that classroom at that time
    for key in student_attend:
        s_id, c_id, r_id, d, h = key
        model.AddImplication(
            student_attend[key],
            schedule[(c_id, r_id, d, h)]
        )

    # Constraint 6: Classroom capacity limits
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

    # Constraint 7: Each student must complete all hours for each course
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

    # Constraint 8: Students can only attend courses in the scheduled time slots
    for s in students:
        for c in courses:
            if c['id'] in s['courseIds']:
                for r in classrooms:
                    if r['type'] == c['roomType']:
                        for d in r['openday']:
                            for h in range(r['opentime'], r['closetime']):
                                if (s['id'], c['id'], r['id'], d, h) in student_attend and (c['id'], r['id'], d, h) in schedule:
                                    model.AddImplication(
                                        student_attend[(s['id'], c['id'], r['id'], d, h)],
                                        schedule[(c['id'], r['id'], d, h)]
                                    )

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Output the result
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Feasible solution found:")

        # Get scheme number incremented by 1, COALESCE: returns 0 if table is NULL
        sql = 'SELECT COALESCE(max("SchemeID"),0) FROM "public"."Schedule";'
        rows = SQLExe(sql, cur)
        SchemeID = rows[0][0] + 1  # Prepare data for insertion

        # Print course schedule
        print("\nCourse schedule:")
        for c in courses:
            print(f"Course {c['name']} (ID: {c['id']}):")
            for r in classrooms:
                for d in r['openday']:
                    for h in range(r['opentime'], r['closetime']):
                        if (c['id'], r['id'], d, h) in schedule and solver.Value(schedule[(c['id'], r['id'], d, h)]):
                            teacher = next((t['name'] for t in teachers if t['id'] == c['teacherId']), 'Unknown')
                            print(f"  {weekdays[d]} Hour {h} in room {r['name']} (Teacher: {teacher})")

                            # Prepare data for insertion
                            CourseTaskID = c['id']
                            CourseTime = h
                            CourseDay = d
                            RoomID = r['id']

                            # Insert scheduling plan
                            sql = ('INSERT INTO "public"."Schedule" ("SchemeID", "CourseTaskID", "Day", "Time", "RoomID", "CampusID", "Semester") VALUES(%d, %d, %d, %d, %d, %d, %d);' % (SchemeID, CourseTaskID, CourseDay, CourseTime, RoomID, CampusID, Semester))
                            cur.execute(sql)
                            conn.commit()

                            students_in_class = [
                                s['name'] for s in students
                                if (s['id'], c['id'], r['id'], d, h) in student_attend and solver.Value(
                                    student_attend[(s['id'], c['id'], r['id'], d, h)])
                            ]
                            print(f"    Students: {', '.join(students_in_class)}")

        # Print teacher schedule
        print("\nTeacher schedule:")
        for t in teachers:
            print(f"Teacher {t['name']} (ID: {t['id']}):")
            for c in courses:
                if c['teacherId'] == t['id']:
                    for r in classrooms:
                        for d in r['openday']:
                            for h in range(r['opentime'], r['closetime']):
                                if (c['id'], r['id'], d, h) in schedule and solver.Value(
                                        schedule[(c['id'], r['id'], d, h)]):
                                    print(f"  {weekdays[d]} Hour {h}: Teach {c['name']} in room {r['name']}")

        # Print student schedule
        print("\nStudent schedule:")
        for s in students:
            print(f"Student {s['name']} (ID: {s['id']}):")
            for c in courses:
                if c['id'] in s['courseIds']:
                    for r in classrooms:
                        for d in r['openday']:
                            for h in range(r['opentime'], r['closetime']):
                                if (s['id'], c['id'], r['id'], d, h) in student_attend and solver.Value(
                                        student_attend[(s['id'], c['id'], r['id'], d, h)]):
                                    teacher = next((t['name'] for t in teachers if t['id'] == c['teacherId']),
                                                   'Unknown')
                                    print(
                                        f"  {weekdays[d]} Hour {h}: Attend {c['name']} in room {r['name']} (Teacher: {teacher})")

        # Course scheduling information query example
        print('Course schedule database query example')
        sql = ('SELECT "Course"."CourseName", "CourseTask"."CourseTaskType", "Teacher"."TeacherName", "Schedule"."Day", "Schedule"."Time", "CourseTask"."TimePerWeek", "Room"."RoomName", "Room"."RoomAddress" \
        FROM "public"."Schedule", "public"."CourseTask", "public"."Room", "public"."Course", "public"."Teacher" \
        WHERE "Schedule"."CourseTaskID" = "CourseTask"."CourseTaskID" AND "Schedule"."RoomID" = "Room"."RoomID" \
        AND "Course"."CourseID" = "CourseTask"."CourseID" AND "CourseTask"."TeacherID" = "Teacher"."TeacherID" \
        AND "Course"."CampusID" = %d AND "Course"."Semester" = %d AND "Schedule"."SchemeID" = %d;' % (CampusID, Semester, SchemeID))
        print(sql)
        rows = SQLExe(sql, cur)
        print('Campus %d, Semester %d, Scheme %d:' % (CampusID, Semester, SchemeID))
        for row in rows:
            CourseSchedule = 'Course: ' + row[0] + ' (' + CouseTypes[row[1]] + '); Teacher: ' + row[2] + '; Every ' + weekdays[row[3]] + \
                            ' from ' + str(row[4]) + ':00 to ' + str(row[4] + row[5]) + ':00; Room: ' + row[6] + '; Address: ' + row[7]
            print(CourseSchedule)

    else:
        print("No feasible solution found.")

    conn.close()

if __name__ == "__main__":
    main()
