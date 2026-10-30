-- University sample database for COSC 431, SQLite version (illustrative data, made up for teaching)
-- Used by the in-browser practice lab. Run with:  sqlite3 university.db < university_sqlite.sql
PRAGMA foreign_keys = ON;

CREATE TABLE department (
  dept_name VARCHAR(40) PRIMARY KEY,
  building  VARCHAR(30) NOT NULL
);

CREATE TABLE student (
  sid   INT PRIMARY KEY,
  name  VARCHAR(60) NOT NULL,
  major VARCHAR(40),
  gpa   DECIMAL(3,2),
  phone VARCHAR(20),
  FOREIGN KEY (major) REFERENCES department(dept_name)
);

CREATE TABLE instructor (
  iid        INT PRIMARY KEY,
  name       VARCHAR(60) NOT NULL,
  dept_name  VARCHAR(40) NOT NULL,
  hired_year INT NOT NULL,
  FOREIGN KEY (dept_name) REFERENCES department(dept_name)
);

CREATE TABLE course (
  course_id VARCHAR(8) PRIMARY KEY,
  title     VARCHAR(60) NOT NULL,
  credits   INT NOT NULL CHECK (credits BETWEEN 1 AND 5),
  dept_name VARCHAR(40) NOT NULL,
  iid       INT,
  FOREIGN KEY (dept_name) REFERENCES department(dept_name),
  FOREIGN KEY (iid) REFERENCES instructor(iid)
);

CREATE TABLE enrollment (
  sid       INT,
  course_id VARCHAR(8),
  term      VARCHAR(12),
  grade     VARCHAR(2),
  PRIMARY KEY (sid, course_id, term),
  FOREIGN KEY (sid) REFERENCES student(sid),
  FOREIGN KEY (course_id) REFERENCES course(course_id)
);

INSERT INTO department VALUES
  ('Computer Science', 'Tech Hall'),
  ('Mathematics',      'Gauss Hall'),
  ('Data Science',     'Tech Hall'),
  ('Physics',          'Curie Hall'),
  ('History',          'Old Main');

INSERT INTO student VALUES
  (1,  'Ada Lovelace',   'Computer Science', 3.90, '555-0101'),
  (2,  'Ben Carter',     'Mathematics',      3.40, NULL),
  (3,  'Carla Diaz',     'Computer Science', 3.70, '555-0103'),
  (4,  'Dev Patel',      'Data Science',     3.20, NULL),
  (5,  'Emma Johnson',   'Computer Science', 3.55, '555-0105'),
  (6,  'Farid Rahman',   'Mathematics',      2.90, '555-0106'),
  (7,  'Grace Kim',      'Data Science',     3.85, '555-0107'),
  (8,  'Hector Alvarez', 'Physics',          3.10, NULL),
  (9,  'Imani Brown',    'Computer Science', NULL, '555-0109'),
  (10, 'Jun Park',       'Data Science',     3.60, '555-0110'),
  (11, 'Kayla Nguyen',   'Mathematics',      3.75, '555-0111'),
  (12, 'Liam O''Connor', NULL,               3.00, NULL);

INSERT INTO instructor VALUES
  (1, 'Amara Okafor',  'Computer Science', 2015),
  (2, 'Luis Romero',   'Computer Science', 2019),
  (3, 'Mei Tanaka',    'Mathematics',      2012),
  (4, 'Samuel Brooks', 'Data Science',     2020),
  (5, 'Hana Petrov',   'Physics',          2010),
  (6, 'Jonah Reyes',   'History',          2017);

INSERT INTO course VALUES
  ('CS101',   'Intro to Programming',    3, 'Computer Science', 1),
  ('CS201',   'Data Structures',         4, 'Computer Science', 2),
  ('CS301',   'Database Management',     3, 'Computer Science', 1),
  ('CS450',   'Special Topics',          3, 'Computer Science', NULL),
  ('MATH101', 'Calculus I',              4, 'Mathematics',      3),
  ('MATH201', 'Linear Algebra',          3, 'Mathematics',      3),
  ('DS110',   'Intro to Data Science',   3, 'Data Science',     4),
  ('DS210',   'Machine Learning',        3, 'Data Science',     4),
  ('PHYS101', 'Physics I',               4, 'Physics',          5),
  ('HIST101', 'World History',           3, 'History',          6);

INSERT INTO enrollment VALUES
  (1,  'CS101',   'Fall 2025', 'A'),  (1,  'MATH101', 'Fall 2025', 'A-'), (1,  'CS201',   'Fall 2026', NULL),
  (2,  'CS101',   'Fall 2025', 'B'),  (2,  'MATH101', 'Fall 2025', 'B+'), (2,  'MATH201', 'Fall 2026', NULL),
  (3,  'CS101',   'Fall 2025', 'A-'), (3,  'CS201',   'Fall 2026', NULL), (3,  'CS301',   'Fall 2026', NULL),
  (4,  'CS101',   'Fall 2025', 'C+'), (4,  'MATH101', 'Fall 2025', 'B'),  (4,  'DS110',   'Fall 2025', 'B+'),
  (5,  'CS101',   'Fall 2025', 'B+'), (5,  'PHYS101', 'Fall 2025', 'B'),  (5,  'CS201',   'Fall 2026', NULL),
  (6,  'MATH101', 'Fall 2025', 'C'),  (6,  'MATH201', 'Fall 2026', NULL),
  (7,  'CS101',   'Fall 2025', 'A'),  (7,  'DS110',   'Fall 2025', 'A'),  (7,  'DS210',   'Fall 2026', NULL),
  (8,  'MATH101', 'Fall 2025', 'B'),  (8,  'PHYS101', 'Fall 2025', 'B-'),
  (10, 'CS101',   'Fall 2025', 'B'),  (10, 'DS110',   'Fall 2025', 'A-'), (10, 'DS210',   'Fall 2026', NULL),
  (11, 'MATH101', 'Fall 2025', 'A'),  (11, 'HIST101', 'Fall 2025', 'A-'), (11, 'MATH201', 'Fall 2026', NULL);
