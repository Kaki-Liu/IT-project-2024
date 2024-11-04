/*
 Navicat Premium Data Transfer

 Source Server         : postgres_db
 Source Server Type    : PostgreSQL
 Source Server Version : 120020
 Source Host           : localhost:65432
 Source Catalog        : Course
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 120020
 File Encoding         : 65001

 Date: 24/10/2024 00:03:07
*/


-- ----------------------------
-- Table structure for Course
-- ----------------------------
DROP TABLE IF EXISTS "public"."Course";
CREATE TABLE "public"."Course" (
  "CourseID" int4 NOT NULL,
  "CourseName" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "Semester" int4 NOT NULL,
  "CampusID" int4 NOT NULL,
  "DeliveryMode" int4 NOT NULL,
  "MajorID" int4 NOT NULL
)
;
COMMENT ON COLUMN "public"."Course"."CourseID" IS '课程ID';
COMMENT ON COLUMN "public"."Course"."CourseName" IS '课程名称';
COMMENT ON COLUMN "public"."Course"."Semester" IS '学期';
COMMENT ON COLUMN "public"."Course"."CampusID" IS '校区ID';
COMMENT ON COLUMN "public"."Course"."DeliveryMode" IS '授课形式，0：线下，1：线上（其他校区）';
COMMENT ON COLUMN "public"."Course"."MajorID" IS '专业ID';
COMMENT ON TABLE "public"."Course" IS '课程列表
记录课程信息。具体任课信息、课时信息由课程任务表记录。

无论授课形式是线上还是线下，都需要分配教室。
线下课程要考虑教室容量；
线上课程无需考虑教室容量，象征性的分配教室即可。
';

-- ----------------------------
-- Records of Course
-- ----------------------------
INSERT INTO "public"."Course" VALUES (1, 'MITS10001', 0, 0, 0, 0);
INSERT INTO "public"."Course" VALUES (2, 'MITS10002', 0, 0, 0, 0);
INSERT INTO "public"."Course" VALUES (3, 'MITS10003', 0, 0, 0, 0);
INSERT INTO "public"."Course" VALUES (4, 'MITS10004', 0, 0, 0, 0);
INSERT INTO "public"."Course" VALUES (5, 'MITS10005', 0, 0, 0, 0);
INSERT INTO "public"."Course" VALUES (6, 'MITS10006', 0, 0, 0, 0);
INSERT INTO "public"."Course" VALUES (7, 'MITS10007', 0, 0, 0, 0);
INSERT INTO "public"."Course" VALUES (8, 'MITS10008', 0, 0, 0, 0);
INSERT INTO "public"."Course" VALUES (9, 'MITS10009', 0, 0, 0, 0);
INSERT INTO "public"."Course" VALUES (10, 'MITS10010', 0, 0, 1, 0);
INSERT INTO "public"."Course" VALUES (11, 'MITS10011', 0, 0, 0, 0);
INSERT INTO "public"."Course" VALUES (12, 'MITS10012', 0, 0, 0, 0);
INSERT INTO "public"."Course" VALUES (13, 'BITS10001', 0, 0, 0, 1);
INSERT INTO "public"."Course" VALUES (14, 'BITS10002', 0, 0, 0, 1);
INSERT INTO "public"."Course" VALUES (15, 'BITS10003', 0, 0, 1, 1);
INSERT INTO "public"."Course" VALUES (16, 'BITS10004', 0, 0, 0, 1);
INSERT INTO "public"."Course" VALUES (17, 'BITS10005', 0, 0, 0, 1);
INSERT INTO "public"."Course" VALUES (18, 'BITS10006', 0, 0, 0, 1);
INSERT INTO "public"."Course" VALUES (19, 'BITS10007', 0, 0, 0, 1);
INSERT INTO "public"."Course" VALUES (20, 'BITS10008', 0, 0, 1, 1);
INSERT INTO "public"."Course" VALUES (21, 'BITS10009', 0, 0, 0, 1);
INSERT INTO "public"."Course" VALUES (22, 'BITS10010', 0, 0, 0, 1);
INSERT INTO "public"."Course" VALUES (23, 'BITS10011', 0, 0, 0, 1);
INSERT INTO "public"."Course" VALUES (24, 'BITS10012', 0, 0, 1, 1);

-- ----------------------------
-- Table structure for CourseSel
-- ----------------------------
DROP TABLE IF EXISTS "public"."CourseSel";
CREATE TABLE "public"."CourseSel" (
  "StudentID" int4 NOT NULL,
  "CourseID" int4 NOT NULL,
  "Semester" int4 NOT NULL,
  "CampusID" int4 NOT NULL
)
;
COMMENT ON COLUMN "public"."CourseSel"."StudentID" IS '学生ID';
COMMENT ON COLUMN "public"."CourseSel"."CourseID" IS '课程ID';
COMMENT ON COLUMN "public"."CourseSel"."Semester" IS '学期';
COMMENT ON COLUMN "public"."CourseSel"."CampusID" IS '校区ID';

-- ----------------------------
-- Records of CourseSel
-- ----------------------------
INSERT INTO "public"."CourseSel" VALUES (0, 3, 0, 0);
INSERT INTO "public"."CourseSel" VALUES (0, 5, 0, 0);
INSERT INTO "public"."CourseSel" VALUES (0, 6, 0, 0);
INSERT INTO "public"."CourseSel" VALUES (0, 9, 0, 0);
INSERT INTO "public"."CourseSel" VALUES (1, 1, 0, 0);
INSERT INTO "public"."CourseSel" VALUES (1, 2, 0, 0);
INSERT INTO "public"."CourseSel" VALUES (1, 3, 0, 0);
INSERT INTO "public"."CourseSel" VALUES (2, 1, 0, 0);
INSERT INTO "public"."CourseSel" VALUES (2, 5, 0, 0);
INSERT INTO "public"."CourseSel" VALUES (2, 6, 0, 0);
INSERT INTO "public"."CourseSel" VALUES (2, 10, 0, 0);
INSERT INTO "public"."CourseSel" VALUES (3, 3, 0, 0);
INSERT INTO "public"."CourseSel" VALUES (3, 8, 0, 0);
INSERT INTO "public"."CourseSel" VALUES (3, 9, 0, 0);
INSERT INTO "public"."CourseSel" VALUES (3, 11, 0, 0);

-- ----------------------------
-- Table structure for CourseTask
-- ----------------------------
DROP TABLE IF EXISTS "public"."CourseTask";
CREATE TABLE "public"."CourseTask" (
  "CourseTaskID" int4 GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "CourseTaskType" int4 NOT NULL,
  "TimePerWeek" int4 NOT NULL,
  "CoherenceRequirement" bool NOT NULL,
  "TeacherID" int4,
  "CourseID" int4 NOT NULL,
  "RoomType" int4,
  "CampusID" int4 NOT NULL
);

COMMENT ON COLUMN "public"."CourseTask"."CourseTaskID" IS '授课任务ID';
COMMENT ON COLUMN "public"."CourseTask"."CourseTaskType" IS '授课形式类型，0讲座、1训练、2试验、3实践，所需教室不同，';
COMMENT ON COLUMN "public"."CourseTask"."TimePerWeek" IS '每周授课时长（小时）';
COMMENT ON COLUMN "public"."CourseTask"."CoherenceRequirement" IS '连贯授课要求，true标是必须一次性连贯授课，不可拆分';
COMMENT ON COLUMN "public"."CourseTask"."TeacherID" IS '任课老师ID';
COMMENT ON COLUMN "public"."CourseTask"."CourseID" IS '课程ID';
COMMENT ON COLUMN "public"."CourseTask"."RoomType" IS '根据课程类型确定教室类型，暂定讲座需要教室，训练、实验、实践都需要实验室';
COMMENT ON TABLE "public"."CourseTask" IS '课程任务表
每个课程分为4种子课程，分别为：讲座、训练、试验、实践，对应不同的功能教室和授课教师。
教师可能负责多门课程，但同一时间只能在1间教室教授1门课程。
不是所有课程都有完整的4门子课程。多数课程只有1~2种子课程。

CoherenceRequirement
连贯授课要求暂定义为：true标是必须一次性连贯授课，不可拆分。
算法初期，默认都为不可拆分课程。';

-- 插入记录时不需要手动指定 CourseTaskID，数据库会自动生成唯一的 CourseTaskID
INSERT INTO "public"."CourseTask" 
    ("CourseTaskType", "TimePerWeek", "CoherenceRequirement", "TeacherID", "CourseID", "RoomType", "CampusID")
VALUES 
(1, 0, 'f', 0, 17, 1, 0),
(1, 0, 'f', 0, 2, 1, 0),
(2, 3, 'f', 0, 7, 1, 0),
(1, 0, 'f', 0, 3, 1, 0),
(1, 3, 'f', 0, 18, 1, 0),
(1, 0, 'f', 0, 4, 1, 0),
(1, 0, 'f', 0, 5, 1, 0),
(2, 1, 'f', 0, 19, 1, 0),
(3, 0, 'f', 2, 9, 1, 0),
(1, 0, 'f', 0, 19, 1, 0),
(1, 0, 'f', 0, 7, 1, 0),
(1, 1, 'f', 0, 8, 1, 0),
(1, 0, 'f', 0, 20, 1, 0),
(1, 0, 'f', 0, 9, 1, 0),
(3, 0, 'f', 0, 7, 1, 0),
(1, 0, 'f', 0, 10, 1, 0),
(1, 1, 'f', 0, 21, 1, 0),
(1, 0, 'f', 0, 11, 1, 0),
(2, 2, 'f', 0, 9, 1, 0),
(1, 1, 'f', 0, 12, 1, 0),
(1, 0, 'f', 0, 22, 1, 0),
(1, 0, 'f', 0, 13, 1, 0),
(2, 0, 'f', 0, 20, 1, 0),
(1, 1, 'f', 0, 23, 1, 0),
(2, 0, 'f', 0, 10, 1, 0),
(1, 0, 'f', 0, 24, 1, 0),
(2, 0, 'f', 0, 21, 1, 0),
(3, 0, 'f', 8, 11, 1, 0),
(3, 0, 'f', 0, 18, 1, 0),
(2, 1, 'f', 0, 2, 1, 0),
(2, 1, 'f', 0, 11, 1, 0),
(2, 1, 'f', 0, 22, 1, 0),
(2, 0, 'f', 0, 4, 1, 0),
(3, 0, 'f', 0, 8, 1, 0),
(2, 1, 'f', 0, 5, 1, 0),
(2, 0, 'f', 0, 12, 1, 0),
(2, 0, 'f', 0, 6, 1, 0),
(2, 0, 'f', 0, 23, 1, 0),
(1, 0, 'f', 8, 14, 1, 0),
(2, 2, 'f', 0, 13, 1, 0),
(2, 2, 'f', 0, 24, 1, 0),
(2, 1, 'f', 0, 15, 1, 0),
(3, 0, 'f', 0, 1, 1, 0),
(2, 0, 'f', 0, 16, 1, 0),
(3, 0, 'f', 0, 19, 1, 0),
(2, 1, 'f', 0, 17, 1, 0),
(2, 0, 'f', 6, 14, 1, 0),
(2, 0, 'f', 0, 18, 1, 0),
(0, 2, 'f', 1, 1, 0, 0),
(2, 0, 'f', 3, 1, 1, 0),
(2, 0, 'f', 5, 3, 1, 0),
(3, 1, 'f', 6, 4, 1, 0),
(1, 2, 'f', 8, 6, 1, 0),
(2, 0, 'f', 9, 8, 1, 0),
(3, 2, 'f', 1, 10, 1, 0),
(0, 1, 'f', 0, 2, 0, 0),
(0, 2, 'f', 0, 3, 0, 0),
(0, 1, 'f', 0, 4, 0, 0),
(0, 1, 'f', 0, 5, 0, 0),
(0, 2, 'f', 0, 6, 0, 0),
(0, 2, 'f', 0, 7, 0, 0),
(0, 1, 'f', 0, 8, 0, 0),
(0, 1, 'f', 0, 9, 0, 0),
(0, 2, 'f', 0, 10, 0, 0),
(0, 2, 'f', 0, 11, 0, 0),
(0, 1, 'f', 0, 12, 0, 0),
(0, 1, 'f', 0, 13, 0, 0),
(0, 2, 'f', 0, 15, 0, 0),
(0, 1, 'f', 0, 16, 0, 0),
(0, 1, 'f', 0, 17, 0, 0),
(0, 2, 'f', 0, 18, 0, 0),
(0, 2, 'f', 0, 19, 0, 0),
(0, 1, 'f', 0, 20, 0, 0),
(0, 2, 'f', 0, 21, 0, 0),
(0, 1, 'f', 0, 22, 0, 0),
(0, 1, 'f', 0, 23, 0, 0),
(0, 2, 'f', 0, 24, 0, 0),
(1, 2, 'f', 0, 1, 1, 0),
(1, 2, 'f', 0, 16, 1, 0);


-- ----------------------------
-- Table structure for Major
-- ----------------------------
DROP TABLE IF EXISTS "public"."Major";
CREATE TABLE "public"."Major" (
  "MajorID" int4 NOT NULL,
  "MajorName" varchar(255) COLLATE "pg_catalog"."default" NOT NULL
)
;
COMMENT ON COLUMN "public"."Major"."MajorID" IS '专业ID';
COMMENT ON COLUMN "public"."Major"."MajorName" IS '专业名称';
COMMENT ON TABLE "public"."Major" IS '专业表';

-- ----------------------------
-- Records of Major
-- ----------------------------
INSERT INTO "public"."Major" VALUES (0, 'MITS');
INSERT INTO "public"."Major" VALUES (1, 'BITS');

-- ----------------------------
-- Table structure for Room
-- ----------------------------

DROP TABLE IF EXISTS "public"."Room";
CREATE TABLE "public"."Room" (
"RoomID" int4 GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
"RoomName" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "RoomType" int4 NOT NULL,
  "RoomCapacity" int4 NOT NULL,
  "RoomAddress" varchar(255) COLLATE "pg_catalog"."default",
  "CampusID" int4 NOT NULL,
  "RoomAvailableTimeStart" int2 NOT NULL,
  "RoomAvailableTimeEnd" int2 NOT NULL,
  "RoomAvailableDays" int2 NOT NULL
);

COMMENT ON COLUMN "public"."Room"."RoomID" IS '教室ID';
COMMENT ON COLUMN "public"."Room"."RoomName" IS '教室名称';
COMMENT ON COLUMN "public"."Room"."RoomType" IS '教室类型，0：教室，1：实验室';
COMMENT ON COLUMN "public"."Room"."RoomCapacity" IS '教室容量';
COMMENT ON COLUMN "public"."Room"."RoomAddress" IS '教室地址';
COMMENT ON COLUMN "public"."Room"."CampusID" IS '校区ID';
COMMENT ON COLUMN "public"."Room"."RoomAvailableTimeStart" IS '每天可用起始时刻，0~23小时';
COMMENT ON COLUMN "public"."Room"."RoomAvailableTimeEnd" IS '每天可用结束时刻，0~23小时';
COMMENT ON COLUMN "public"."Room"."RoomAvailableDays" IS '每周可用日';
COMMENT ON TABLE "public"."Room" IS '教室表

每周可用日按bit置位，bit0是周日
# 星期映射表
weekdays = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday"
}';

-- 插入记录时不需要手动指定 RoomID，数据库会自动生成唯一的 RoomID
INSERT INTO "public"."Room" 
    ("RoomName", "RoomType", "RoomCapacity", "RoomAddress", "CampusID", "RoomAvailableTimeStart", "RoomAvailableTimeEnd", "RoomAvailableDays")
VALUES 
    ('CLASSROOM 7-1', 0, 40, 'Building A, Floor 1, CLASSROOM 7-1', 0, 8, 17, 42),
    ('LAB 1-5', 1, 30, 'Building B, Floor 3, LAB 1-5', 0, 9, 18, 42),
    ('CLASSROOM 2-1', 0, 50, 'Building A, Floor 1, CLASSROOM 2-1', 0, 8, 12, 20),
    ('LAB 9-8', 1, 25, 'Building C, Floor 2, LAB 9-8', 0, 8, 16, 26),
    ('CLASSROOM 3-2', 0, 45, 'Building A, Floor 1, CLASSROOM 3-2', 0, 8, 17, 42),
    ('LAB 9-7', 1, 35, 'Building B, Floor 3, LAB 9-7', 0, 10, 18, 50),
    ('CLASSROOM 5-4', 0, 60, 'Building A, Floor 2, CLASSROOM 5-4', 0, 8, 17, 22),
    ('LAB 2-2', 1, 20, 'Building D, Floor 1, LAB 2-2', 0, 9, 17, 28),
    ('CLASSROOM 6-1', 0, 55, 'Building A, Floor 1, CLASSROOM 6-1', 0, 8, 12, 40),
    ('LAB 1-2', 1, 28, 'Building C, Floor 3, LAB 1-2', 0, 9, 16, 20);

-- ----------------------------
-- Table structure for Schedule
-- ----------------------------
DROP TABLE IF EXISTS "public"."Schedule";
CREATE TABLE "public"."Schedule" (
  "SchemeID" int4 NOT NULL,
  "CourseTaskID" int4 NOT NULL,
  "Day" int4 NOT NULL,
  "Time" int4 NOT NULL,
  "RoomID" int4 NOT NULL,
  "CampusID" int4 NOT NULL,
  "Semester" int4 NOT NULL
)
;
COMMENT ON COLUMN "public"."Schedule"."SchemeID" IS '排课方案序号';
COMMENT ON COLUMN "public"."Schedule"."CourseTaskID" IS '子课程ID';
COMMENT ON COLUMN "public"."Schedule"."Day" IS '上课星期';
COMMENT ON COLUMN "public"."Schedule"."Time" IS '开始上课时间（时长按课程要求一次上完）';
COMMENT ON COLUMN "public"."Schedule"."RoomID" IS '上课教室';
COMMENT ON COLUMN "public"."Schedule"."CampusID" IS '校区';
COMMENT ON COLUMN "public"."Schedule"."Semester" IS '学期';

-- ----------------------------
-- Records of Schedule
-- ----------------------------
INSERT INTO "public"."Schedule" VALUES (1, 0, 1, 16, 1, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 0, 3, 8, 1, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 1, 5, 13, 1, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 2, 4, 8, 3, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 2, 1, 15, 5, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 4, 3, 9, 1, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 5, 1, 13, 1, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 5, 4, 12, 7, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 7, 5, 9, 1, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 8, 1, 10, 5, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 9, 5, 15, 5, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 9, 5, 10, 9, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 10, 1, 8, 5, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 10, 1, 12, 5, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 24, 3, 17, 2, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 24, 5, 16, 6, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 29, 2, 13, 8, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 29, 3, 13, 8, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 31, 4, 10, 4, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 49, 4, 16, 8, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 52, 3, 15, 4, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 56, 3, 16, 2, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 56, 3, 12, 4, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 58, 4, 9, 10, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 74, 3, 10, 2, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 74, 5, 14, 6, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 81, 1, 9, 2, 0, 0);
INSERT INTO "public"."Schedule" VALUES (1, 81, 4, 11, 4, 0, 0);

-- ----------------------------
-- Table structure for Student
-- ----------------------------
DROP TABLE IF EXISTS "public"."Student";
CREATE TABLE "public"."Student" (
  "StudentID" int4 NOT NULL,
  "MajorID" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "CampusID" int4 NOT NULL,
  "StudentName" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "SchoolNumber" int4,
  "StudentValid" bool NOT NULL,
  "StudentType" varchar(255) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."Student"."StudentID" IS '学生ID';
COMMENT ON COLUMN "public"."Student"."MajorID" IS '专业ID';
COMMENT ON COLUMN "public"."Student"."CampusID" IS '校区ID';
COMMENT ON COLUMN "public"."Student"."StudentName" IS '姓名';
COMMENT ON COLUMN "public"."Student"."SchoolNumber" IS '学号';
COMMENT ON COLUMN "public"."Student"."StudentValid" IS '学生是否有效，比如已经毕业，未入学';
COMMENT ON COLUMN "public"."Student"."StudentType" IS '学生类型';

-- ----------------------------
-- Records of Student
-- ----------------------------
INSERT INTO "public"."Student" VALUES (2, '0', 0, 'Vo', 9101, 't', 'CRICOS Onshore Enrolment');
INSERT INTO "public"."Student" VALUES (3, '0', 0, 'Robert', 1213, 't', 'CRICOS Onshore Enrolment');
INSERT INTO "public"."Student" VALUES (0, '0', 0, 'Saurabh Mehta', 1234, 't', 'CRICOS Onshore Enrolment
');
INSERT INTO "public"."Student" VALUES (1, '0', 0, 'Kalindi', 5678, 't', 'CRICOS Onshore Enrolment');

-- ----------------------------
-- Table structure for Teacher
-- ----------------------------
DROP TABLE IF EXISTS "public"."Teacher";
CREATE TABLE "public"."Teacher" (
  "TeacherID" int4 NOT NULL,
  "TeacherName" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "TeacherAbility" varchar(255) COLLATE "pg_catalog"."default",
  "CampusID" int4 NOT NULL,
  "MajorID" int4,
  "TeacherType" int2 NOT NULL
)
;
COMMENT ON COLUMN "public"."Teacher"."TeacherID" IS '教师ID';
COMMENT ON COLUMN "public"."Teacher"."TeacherName" IS '教师姓名';
COMMENT ON COLUMN "public"."Teacher"."TeacherAbility" IS '暂时不用，教师教学能力，用于表示可以教哪类课';
COMMENT ON COLUMN "public"."Teacher"."CampusID" IS '校区ID';
COMMENT ON COLUMN "public"."Teacher"."MajorID" IS '专业ID';
COMMENT ON COLUMN "public"."Teacher"."TeacherType" IS '教师类型，0：讲师，1：试验助手';
COMMENT ON TABLE "public"."Teacher" IS '教师表

TeacherAbility：任教能力暂时不用

MajorID：暂不清楚教师是否要属于某专业';

-- ----------------------------
-- Records of Teacher
-- ----------------------------
INSERT INTO "public"."Teacher" VALUES (0, 'Daniel Miller', '0', 0, 0, 0);
INSERT INTO "public"."Teacher" VALUES (1, 'Samuel Johnson', '0', 0, 0, 0);
INSERT INTO "public"."Teacher" VALUES (2, 'Christopher Davis', '0', 0, 0, 0);
INSERT INTO "public"."Teacher" VALUES (3, 'Matthew Smith', '0', 0, 0, 0);
INSERT INTO "public"."Teacher" VALUES (4, 'Olivia Johnson', '0', 0, 0, 0);
INSERT INTO "public"."Teacher" VALUES (5, 'David Gonzalez', '0', 0, 0, 0);
INSERT INTO "public"."Teacher" VALUES (6, 'Jane Anderson', '0', 0, 0, 0);
INSERT INTO "public"."Teacher" VALUES (7, 'James Lee', '0', 0, 0, 0);
INSERT INTO "public"."Teacher" VALUES (8, 'Emily Perez', '0', 0, 0, 0);
INSERT INTO "public"."Teacher" VALUES (9, 'John Taylor', '0', 0, 0, 0);
INSERT INTO "public"."Teacher" VALUES (10, 'Alexander Lopez', '0', 0, 0, 0);
INSERT INTO "public"."Teacher" VALUES (11, 'Jack Thompson', '0', 0, 0, 0);
INSERT INTO "public"."Teacher" VALUES (12, 'Jack Wilson', '0', 0, 0, 1);
INSERT INTO "public"."Teacher" VALUES (13, 'Amelia Gonzalez', '0', 0, 0, 1);
INSERT INTO "public"."Teacher" VALUES (14, 'Samuel Anderson', '0', 0, 0, 1);
INSERT INTO "public"."Teacher" VALUES (15, 'William Brown', '0', 0, 0, 1);
INSERT INTO "public"."Teacher" VALUES (16, 'Harper Jackson', '0', 0, 0, 1);
INSERT INTO "public"."Teacher" VALUES (17, 'Olivia Thompson', '0', 0, 0, 1);
INSERT INTO "public"."Teacher" VALUES (18, 'Christopher White', '0', 0, 0, 1);
INSERT INTO "public"."Teacher" VALUES (19, 'Henry Moore', '0', 0, 0, 1);
INSERT INTO "public"."Teacher" VALUES (20, 'Emily Davis', '0', 0, 0, 1);
INSERT INTO "public"."Teacher" VALUES (21, 'Michael Rodriguez', '0', 0, 0, 1);
INSERT INTO "public"."Teacher" VALUES (22, 'Charlotte Smith', '0', 0, 0, 1);
INSERT INTO "public"."Teacher" VALUES (23, 'Jane Lee', '0', 0, 0, 1);
INSERT INTO "public"."Teacher" VALUES (24, 'Sophia Martinez', '0', 0, 1, 0);
INSERT INTO "public"."Teacher" VALUES (25, 'Mia Brown', '0', 0, 1, 0);
INSERT INTO "public"."Teacher" VALUES (26, 'Emma White', '0', 0, 1, 0);
INSERT INTO "public"."Teacher" VALUES (27, 'Henry Rodriguez', '0', 0, 1, 0);
INSERT INTO "public"."Teacher" VALUES (28, 'Amelia Wilson', '0', 0, 1, 0);
INSERT INTO "public"."Teacher" VALUES (29, 'William Davis', '0', 0, 1, 0);
INSERT INTO "public"."Teacher" VALUES (30, 'Charlotte Thomas', '0', 0, 1, 0);
INSERT INTO "public"."Teacher" VALUES (31, 'Evelyn Jackson', '0', 0, 1, 0);
INSERT INTO "public"."Teacher" VALUES (32, 'Michael Hernandez', '0', 0, 1, 0);
INSERT INTO "public"."Teacher" VALUES (33, 'Harper Moore', '0', 0, 1, 0);
INSERT INTO "public"."Teacher" VALUES (34, 'Isabella Miller', '0', 0, 1, 0);
INSERT INTO "public"."Teacher" VALUES (35, 'Ava Garcia', '0', 0, 1, 0);
INSERT INTO "public"."Teacher" VALUES (36, 'Mia Hernandez', '0', 0, 1, 1);
INSERT INTO "public"."Teacher" VALUES (37, 'James Johnson', '0', 0, 1, 1);
INSERT INTO "public"."Teacher" VALUES (38, 'John Taylor', '0', 0, 1, 1);
INSERT INTO "public"."Teacher" VALUES (39, 'Alexander Wilson', '0', 0, 1, 1);
INSERT INTO "public"."Teacher" VALUES (40, 'Sophia Davis', '0', 0, 1, 1);
INSERT INTO "public"."Teacher" VALUES (41, 'Matthew Lopez', '0', 0, 1, 1);
INSERT INTO "public"."Teacher" VALUES (42, 'Isabella Miller', '0', 0, 1, 1);
INSERT INTO "public"."Teacher" VALUES (43, 'David Jackson', '0', 0, 1, 1);
INSERT INTO "public"."Teacher" VALUES (44, 'Daniel Martin', '0', 0, 1, 1);
INSERT INTO "public"."Teacher" VALUES (45, 'Emma Martinez', '0', 0, 1, 1);
INSERT INTO "public"."Teacher" VALUES (46, 'Ava Perez', '0', 0, 1, 1);
INSERT INTO "public"."Teacher" VALUES (47, 'Evelyn Johnson', '0', 0, 1, 1);

CREATE TABLE "public"."NewSchedule" AS
        SELECT 
            sch."SchemeID",
            sch."Day",
            sch."Time" AS "StartTime",
            (sch."Time" + ct."TimePerWeek") AS "EndTime",
            c."CourseName",
            r."RoomName",
            r."RoomAddress",
            sch."CampusID"
        FROM 
            "public"."Schedule" sch
        JOIN 
            "public"."CourseTask" ct ON sch."CourseTaskID" = ct."CourseTaskID"
        JOIN 
            "public"."Course" c ON ct."CourseID" = c."CourseID"
        JOIN 
            "public"."Room" r ON sch."RoomID" = r."RoomID"
        WHERE 
            ct."TimePerWeek" > 0;


-- -- ----------------------------
-- -- Primary Key structure for table Teacher
-- -- ----------------------------
-- ALTER TABLE "public"."Teacher" ADD CONSTRAINT "Teacher_pkey" PRIMARY KEY ("TeacherID");
