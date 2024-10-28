from ortools.sat.python import cp_model
import json

# Weekday mapping
weekdays = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday"
}

def main():
    # Read input data
    with open('input.json', 'r') as f:
        data = json.load(f)

    courses = data['courses']
    classrooms = data['classrooms']
    students = data['students']
    teachers = data['teachers']

    # Create the CSP model
    model = cp_model.CpModel()

    # Get all possible time slots and classroom combinations
    time_slots = []
    for r in classrooms:
        for d in r['openday']:
            for h in range(r['opentime'], r['closetime']):
                time_slots.append((r['id'], d, h))

    # Create possible scheduling variables for each course
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

    # Calculate the minimum number of groups needed to meet the classroom capacity constraint for each course
    course_students = {}
    for c in courses:
        enrolled_students = [s for s in students if c['id'] in s['courseIds']]
        course_students[c['id']] = enrolled_students

    # Constraint 1: Courses must be scheduled within the open hours and classrooms
    for c in courses:
        total_hours = c['weeklyHours']
        possible_slots = [key for key in schedule if key[0] == c['id']]
        model.Add(
            sum(schedule[key] for key in possible_slots) == total_hours
        )

    # Constraint 2: Only one course can be scheduled in a classroom at the same time
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

    # Constraint 3: Teachers can only teach one course at a time
    for t in teachers:
        for d in range(1, 6):
            for h in range(8, 22):  # Assume all classrooms are open between 8 AM and 10 PM
                model.Add(
                    sum(
                        schedule[(c['id'], r['id'], d, h)]
                        for c in courses if c['teacherId'] == t['id']
                        for r in classrooms if (c['id'], r['id'], d, h) in schedule
                    ) <= 1
                )

    # Constraint 4: Students can only attend one course at a time
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

    # Constraint 5: If a student attends a course at a certain time, the course must be scheduled in that classroom
    for key in student_attend:
        s_id, c_id, r_id, d, h = key
        model.AddImplication(
            student_attend[key],
            schedule[(c_id, r_id, d, h)]
        )

    # Constraint 6: Classroom capacity limit
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

    # Constraint 7: Each student must complete all weekly hours for each course they are enrolled in
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

    # Constraint 8: Students can only attend courses during scheduled hours
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

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Output the results
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Found a feasible solution:")

        # Print course schedule
        print("\nCourse Schedule:")
        for c in courses:
            print(f"Course {c['name']} (ID: {c['id']}):")
            for r in classrooms:
                for d in r['openday']:
                    for h in range(r['opentime'], r['closetime']):
                        if (c['id'], r['id'], d, h) in schedule and solver.Value(schedule[(c['id'], r['id'], d, h)]):
                            teacher = next((t['name'] for t in teachers if t['id'] == c['teacherId']), 'Unknown')
                            print(f"  {weekdays[d]} Period {h} in classroom {r['name']} (Teacher: {teacher})")
                            students_in_class = [
                                s['name'] for s in students
                                if (s['id'], c['id'], r['id'], d, h) in student_attend and solver.Value(
                                    student_attend[(s['id'], c['id'], r['id'], d, h)])
                            ]
                            print(f"    Students: {', '.join(students_in_class)}")

        # Print teacher schedule
        print("\nTeacher Schedule:")
        for t in teachers:
            print(f"Teacher {t['name']} (ID: {t['id']}):")
            for c in courses:
                if c['teacherId'] == t['id']:
                    for r in classrooms:
                        for d in r['openday']:
                            for h in range(r['opentime'], r['closetime']):
                                if (c['id'], r['id'], d, h) in schedule and solver.Value(schedule[(c['id'], r['id'], d, h)]):
                                    print(f"  {weekdays[d]} Period {h} teaching {c['name']} in classroom {r['name']}")

        # Print student schedule
        print("\nStudent Schedule:")
        for s in students:
            print(f"Student {s['name']} (ID: {s['id']}):")
            for c in courses:
                if c['id'] in s['courseIds']:
                    for r in classrooms:
                        for d in r['openday']:
                            for h in range(r['opentime'], r['closetime']):
                                if (s['id'], c['id'], r['id'], d, h) in student_attend and solver.Value(
                                        student_attend[(s['id'], c['id'], r['id'], d, h)]):
                                    teacher = next((t['name'] for t in teachers if t['id'] == c['teacherId']), 'Unknown')
                                    print(f"  {weekdays[d]} Period {h} taking {c['name']} in classroom {r['name']} (Teacher: {teacher})")
    else:
        print("No feasible solution found.")

if __name__ == "__main__":
    main()