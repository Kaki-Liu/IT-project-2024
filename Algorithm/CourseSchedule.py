import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import random
import copy
from dateutil import rrule
import datetime
import csv

class Schedule:
    def __init__(self, course_id, class_id, teacher_id, unit_id):
        self.course_id = course_id
        self.class_id = class_id
        self.teacher_id = teacher_id
        self.unit_id = unit_id
        self.time = 0
        self.room_id = 0
        self.tool = -1

    def random_init(self, time, plan):
        self.random_room(plan)
        self.random_tool(plan)
        self.time = time

    def random_room(self, plan):
        type_id = plan.courses[self.course_id]["typeId"]
        self.room_id = np.random.choice(plan.room_type[type_id])

    def random_tool(self, plan):
        if "toolsCode" in plan.courses[self.course_id]:
            if isinstance(plan.courses[self.course_id]["toolsCode"], list):
                self.tool = np.random.choice(plan.courses[self.course_id]["toolsCode"])
            else:
                self.tool = plan.courses[self.course_id]["toolsCode"]
        else:
            self.tool = -1

class GeneticOptimize:
    def __init__(self, popsize=64, mutprob=0.5, elite=16, maxiter=500):
        self.popsize = popsize
        self.mutprob = mutprob
        self.elite = elite
        self.maxiter = maxiter

    def init_population(self, schedules, plan):
        self.population = []
        self.times_sum = plan.times_sum
        for _ in range(self.popsize):
            entity = []
            for subject in schedules:
                a = random.sample(range(plan.times_sum), subject["subtime_sum"])
                a.sort()
                for count in range(subject["subtime_sum"]):
                    subject["course"][count].random_init(a[count], plan)
            self.population.append(copy.deepcopy(schedules))

    def mutate(self, elite_population, room_range, slot_num, plan):
        e = np.random.randint(0, self.elite)
        ep = copy.deepcopy(elite_population[e])
        for subject in ep:
            pos = np.random.randint(0, 3)
            if pos == 0:
                self.time_change(subject)
            elif pos == 1:
                self.room_change(subject, plan)
            else:
                self.tool_change(subject, plan)
        return ep

    def time_change(self, subject):
        time_mutate_rate = 0.2
        lesson_length = subject["subtime_sum"]
        mutate_num = int(lesson_length * time_mutate_rate)
        b = random.sample(range(lesson_length), mutate_num)
        for i in b:
            if i == 0:
                start = -1
                end = subject["course"][i + 1].time
            elif i == lesson_length - 1:
                start = subject["course"][i - 1].time
                end = self.times_sum
            else:
                start = subject["course"][i - 1].time
                end = subject["course"][i + 1].time
            time = np.random.randint(start + 1, end)
            subject["course"][i].time = time

    def room_change(self, subject, plan):
        for i in range(subject["subtime_sum"]):
            subject["course"][i].random_room(plan)

    def tool_change(self, subject, plan):
        for i in range(subject["subtime_sum"]):
            subject["course"][i].random_tool(plan)

    def crossover(self, elite_population):
        e1, e2 = np.random.randint(0, self.elite, 2)
        pos = np.random.randint(0, 3)
        ep1 = copy.deepcopy(elite_population[e1])
        ep2 = elite_population[e2]

        for i in range(len(ep1)):
            length = ep1[i]["subtime_sum"]
            if pos == 0:
                for j in range(length):
                    ep1[i]["course"][j].time = ep2[i]["course"][j].time
            elif pos == 1:
                for j in range(length):
                    ep1[i]["course"][j].room_id = ep2[i]["course"][j].room_id
            else:
                for j in range(length):
                    if ep1[i]["course"][j].tool != -1:
                        ep1[i]["course"][j].tool = ep2[i]["course"][j].tool
        return ep1

    def evolution(self, schedules, room_range, slot_num, plan):
        best_score = 0
        best_schedule = None
        self.init_population(schedules, plan)
        self.toolcode2num = plan.toolcode2num
        for i in range(self.maxiter):
            elite_index, best_score = self.schedule_cost(self.population, self.elite)
            print(f'Iter: {i + 1} | conflict: {best_score}')
            if best_score == 0:
                best_schedule = self.population[elite_index[0]]
                break
            new_population = [self.population[index] for index in elite_index]
            while len(new_population) < self.popsize:
                if np.random.rand() < self.mutprob:
                    newp = self.mutate(new_population, room_range, slot_num, plan)
                else:
                    newp = self.crossover(new_population)
                new_population.append(newp)
            self.population = new_population

        success_mark = 1
        if best_schedule is None:
            best_schedule = self.population[elite_index[0]]
            success_mark = 0
        return best_schedule, success_mark

    def schedule_cost(self, population, elite):
        conflicts = []
        for entity in population:
            time_list = [None] * self.times_sum
            for subject in entity:
                teacher_id = subject["teacher"]
                for lesson in subject["course"]:
                    time = lesson.time
                    toolcode = lesson.tool
                    classroom = lesson.room_id
                    if time_list[time] is None:
                        time_list[time] = {"teacherId": {}, "toolcode": {}, "roomId": {}}
                    time_list[time]["teacherId"][teacher_id] = time_list[time]["teacherId"].get(teacher_id, 0) + 1
                    time_list[time]["toolcode"][toolcode] = time_list[time]["toolcode"].get(toolcode, 0) + 1
                    time_list[time]["roomId"][classroom] = time_list[time]["roomId"].get(classroom, 0) + 1
            score = 0
            for time in time_list:
                if time:
                    for teacher_id in time["teacherId"]:
                        score += time["teacherId"][teacher_id] - 1
                    for classroom in time["roomId"]:
                        score += time["roomId"][classroom] - 1
                    for toolcode in time["toolcode"]:
                        if toolcode != -1:
                            if time["toolcode"][toolcode] > self.toolcode2num[toolcode]:
                                score += time["toolcode"][toolcode] - self.toolcode2num[toolcode]
            conflicts.append(score)
        index = np.array(conflicts).argsort()
        return index[:elite], conflicts[index[0]]

class Generation:
    def __init__(self, input_file):
        self.load_data(input_file)
        self.subject_info()
        self.schedule_info_read()
        self.tool_info()
        self.room_info()

    def load_data(self, input_file):
        data = pd.read_csv(input_file)
        self.students = data[data['type'] == 'student'].to_dict('records')
        self.teachers = data[data['type'] == 'teacher'].to_dict('records')
        self.classroom = data[data['type'] == 'classroom'].to_dict('records')
        self.subject = data[data['type'] == 'subject'].to_dict('records')
        self.courses = data[data['type'] == 'course'].to_dict('records')
        self.tools = data[data['type'] == 'tool'].to_dict('records')
        self.schedule = data[data['type'] == 'schedule'].iloc[0].to_dict()

    def schedule_info_read(self):
        week_on = [int(self.schedule[day]) for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]]
        lesson_num_am = int(self.schedule["lessonNumAm"])
        lesson_num_pm = int(self.schedule["lessonNumPm"])

        week_mask = " ".join([["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][i] for i, v in enumerate(week_on) if v != 0])

        s_day = datetime.datetime.strptime(self.schedule["startTermBegin"], "%Y-%m-%d")
        e_day = datetime.datetime.strptime(self.schedule["startTermEnd"], "%Y-%m-%d")
        bus_day = list(rrule.rrule(rrule.DAILY, dtstart=s_day, until=e_day, byweekday=[0,1,2,3,4,5,6]))

        day_period = []
        times_sum = 0
        for day in bus_day:
            weekday = day.weekday()
            if week_on[weekday] == 1:
                times = lesson_num_am + lesson_num_pm
            elif week_on[weekday] == 2:
                times = lesson_num_am
            elif week_on[weekday] == 3:
                times = lesson_num_pm
            else:
                times = 0
            times_sum += times
            day_period.append(times_sum)

        self.bus_day = bus_day
        self.day_period = day_period
        self.times_sum = times_sum
        self.week_on = week_on
        self.lesson_num_am = lesson_num_am
        self.lesson_num_pm = lesson_num_pm

    def subject_info(self):
        subject = {}
        for i in self.subject:
            subject_id = i["subjectId"]
            subject[subject_id] = {
                "subjectNumber": i["subjectNumber"],
                "subjectName": i["subjectName"],
                "teacher": [],
                "course": []
            }
        self.subject = subject
        self.teacher_info()
        self.course_info()

    def teacher_info(self):
        self.teacher_num = len(self.teachers)
        for i, teacher in enumerate(self.teachers):
            sub = teacher["subjectId"]
            if isinstance(sub, list):
                for j in sub:
                    if j in self.subject:
                        self.subject[j]["teacher"].append(i)
                    else:
                        print(f"Teacher {i} has no course")
            else:
                if sub in self.subject:
                    self.subject[sub]["teacher"].append(i)
                else:
                    print(f"Teacher {i} has no course")
            teacher["workload"] = 0
            teacher["subject"] = []

    def course_info(self):
        for i, course in enumerate(self.courses):
            sub_id = course["subjectId"]
            if sub_id in self.subject:
                self.subject[sub_id]["course"].append(i)
            else:
                print(f"Course {i} is not in subjects")
        self.id2course()

    def room_info(self):
        room_type = {}
        for i, room in enumerate(self.classroom):
            if room["typeId"] in room_type:
                room_type[room["typeId"]].append(i)
            else:
                room_type[room["typeId"]] = [i]
        self.room_type = room_type

    def tool_info(self):
        self.toolcode2num = {tool["code"]: tool["count"] for tool in self.tools}

    def id2course(self):
        p = {}
        for i, course in enumerate(self.courses):
            goal_id = course['goalId']
            if isinstance(goal_id, list):
                for j in goal_id:
                    if j in p:
                        p[j].append(i)
                    else:
                        p[j] = [i]
            else:
                if goal_id in p:
                    p[goal_id].append(i)
                else:
                    p[goal_id] = [i]
        self.goalid2course = p
        return p

    def arrange(self):
        cluster_num = 4
        clustering = Cluster(self, cluster_num)
        subject_arrange = []

        for cluster_id, cluster in self.cluster_dict.items():
            for subject_id, course_list in cluster["sub2cou"].items():
                sub_times = cluster["sub_times"][subject_id]
                subtime_sum = sub_times[-1]
                a = random.sample(range(self.times_sum), subtime_sum)
                a.sort()

                subject = {
                    "cluster": cluster_id,
                    "subjectId": subject_id,
                    "subtime_sum": subtime_sum,
                    "teacher": min(range(len(self.teachers)), key=lambda i: self.teachers[i]["workload"]),
                    "course": []
                }

                for course in course_list:
                    for _ in range(self.courses[course]["period"]):
                        b = Schedule(course, cluster_id, subject["teacher"], self.courses[course]["unitId"])
                        subject["course"].append(b)

                subject_arrange.append(subject)

        return subject_arrange

class Cluster:
    def __init__(self, plan, cluster_num=3):
        self.clustering(plan, cluster_num)
        self.cluster_goalid_generate(plan)
        self.subject_arrange(plan)

    @staticmethod
    def embedding_build(plan):
        student_num = len(plan.students)
        goal_max = 1000
        std_embedding = np.zeros([student_num, goal_max])
        for i, student in enumerate(plan.students):
            goal_id = student["goalId"]
            if isinstance(goal_id, list):
                for j in goal_id:
                    std_embedding[i, j] = 1
            else:
                std_embedding[i, goal_id] = 1
        return student_num, std_embedding

    def clustering(self, plan, clusters):
        std_num, embedding = self.embedding_build(plan)
        if std_num > clusters:
            kmeans = KMeans(n_clusters=clusters, random_state=0, init='k-means++').fit(embedding)
            label_list = kmeans.labels_
        else:
            label_list = range(std_num)

        cluster_dict = {}
        for i, label in enumerate(label_list):
            plan.students[i]["label"] = label
            if label in cluster_dict:
                cluster_dict[label]["students"].append(i)
            else:
                cluster_dict[label] = {"students": [i]}

        plan.cluster_dict = cluster_dict

    def cluster_goalid_generate(self, plan):
        for cluster in plan.cluster_dict.values():
            cluster["goalId"] = sorted(set(sum((plan.students[j]["goalId"] for j in cluster["students"]), [])))

    def subject_arrange(self, plan):
        for cluster in plan.cluster_dict.values():
            cluster_course = set()
            for goal_id in cluster["goalId"]:
                if goal_id not in plan.goalid2course:
                    print(f"Goal {goal_id} has no course")
                    continue
                cluster_course.update(plan.goalid2course[goal_id])

            cluster["sub2cou"] = {}
            cluster["sub_times"] = {}
            for subject_id, subject in plan.subject.items():
                sub_cor_set = set(subject["course"])
                temp = sorted(cluster_course & sub_cor_set)
                if temp:
                    subject_times = []
                    times = 0
                    length = len(temp)
                    count = 0
                    temp1 = []
                    while times < subject["subjectNumber"]:
                        times += plan.courses[temp[count]]["period"]
                        subject_times.append(times)
                        temp1.append(temp[count])
                        count = (count + 1) % length
                    cluster["sub2cou"][subject_id] = temp1
                    cluster["sub_times"][subject_id] = subject_times

def result_display(schedules, plan, success_mark):
    time_list = [[] for _ in range(plan.times_sum)]
    for subject in schedules:
        teacher = subject["teacher"]
        cluster = subject["cluster"]
        subject_id = subject["subjectId"]
        for course in subject["course"]:
            time = course.time
            room = course.room_id
            toolcode = course.tool
            course_id = course.course_id
            lesson = {
                "cluster": cluster,
                "teacher": plan.teachers[teacher]["teacherId"],
                "lessonNo": plan.courses[course_id]["lessonNo"],
                "classroomNo": plan.classroom[room]["classroomCode"],
                "unitId": course.unit_id,
                "subjectId": subject_id
            }
            if toolcode != -1:
                lesson["tool"] = toolcode
            time_list[time].append(lesson)

    time_table_list = []
    lesson_count = 1
    for day_count, day_bound in enumerate(plan.day_period):
        for time in range(day_bound - (plan.day_period[day_count-1] if day_count > 0 else 0)):
            if time_list[time]:
                for lesson in time_list[time]:
                    date = plan.bus_day[day_count]
                    day1 = (date - plan.bus_day[0]).days
                    days_of_week = date.weekday() + 1
                    week_no = rrule.rrule(rrule.WEEKLY, dtstart=plan.bus_day[0], until=date).count()
                    tmp_class_id = f'{lesson["cluster"]:015d}'

                    no_of_day = time + 1
                    if plan.week_on[week_no] == 1:
                        time_period = 3 if no_of_day > plan.lesson_num_am else 2
                    elif plan.week_on[week_no] == 2:
                        time_period = 2
                    elif plan.week_on[week_no] == 3:
                        time_period = 3

                    new_dict = {
                        "gradeId": 0,
                        "lessonNo": lesson["lessonNo"],
                        "noOfDay": no_of_day,
                        "adjustType": 0,
                        "sortNumber": lesson_count,
                        "classroomId": lesson["classroomNo"],
                        "daysOfWeek": days_of_week,
                        "subjectId": lesson["subjectId"],
                        "orgId": plan.schedule["orgId"],
                        "classTime": no_of_day + (plan.lesson_num_pm + plan.lesson_num_am) * day1,
                        "teacherId": lesson["teacher"],
                        "scheduleType": 2,
                        "weeksSum": 1,
                        "scheduleDay": date.strftime("%Y-%m-%d"),
                        "timePeriod": time_period,
                        "unitId": lesson["unitId"],
                        "semester": plan.schedule["semester"],
                        "weekNo": week_no,
                        "startTime": "00:00:00",
                        "endTime": "00:00:00",
                        "tmpClassId": tmp_class_id,
                        "statusFlag": 1
                    }

                    time_table_list.append(new_dict)
                    lesson_count += 1

    result = {
        "code": 200 if success_mark == 1 else 400,
        "msg": "success" if success_mark == 1 else "fail",
        "data": {"timeTableList": time_table_list}
    }

    with open('result.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=time_table_list[0].keys())
        writer.writeheader()
        writer.writerows(time_table_list)

    return time_list

def main():
    plan = Generation('input.csv')
    schedules = plan.arrange()
    ga = GeneticOptimize()
    best_schedule, success_mark = ga.evolution(schedules=schedules, room_range=5, slot_num=19, plan=plan)
    result_display(best_schedule, plan, success_mark)

if __name__ == "__main__":
    main()