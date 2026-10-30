-- Relational model demo database for COSC 431 Module 2 (illustrative data, made up for teaching)
-- Run in MySQL 8.4. Drops and recreates the database m2_demo.
DROP DATABASE IF EXISTS m2_demo;
CREATE DATABASE m2_demo;
USE m2_demo;

CREATE TABLE department (
  dept_id   INT PRIMARY KEY,
  dept_name VARCHAR(30) NOT NULL UNIQUE
);
CREATE TABLE student (
  sid     INT PRIMARY KEY,
  name    VARCHAR(40) NOT NULL,
  email   VARCHAR(50) NOT NULL UNIQUE,
  dept_id INT,
  gpa     DECIMAL(3,2),
  CONSTRAINT gpa_range CHECK (gpa BETWEEN 0 AND 4),
  CONSTRAINT fk_student_dept FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);
CREATE TABLE course (
  cid   VARCHAR(8) PRIMARY KEY,
  title VARCHAR(50) NOT NULL
);
CREATE TABLE enrolled (
  sid   INT,
  cid   VARCHAR(8),
  grade CHAR(1),
  PRIMARY KEY (sid, cid),
  CONSTRAINT fk_enr_student FOREIGN KEY (sid) REFERENCES student(sid) ON DELETE CASCADE,
  CONSTRAINT fk_enr_course  FOREIGN KEY (cid) REFERENCES course(cid)
);

INSERT INTO department VALUES (1,'Computer Science'),(2,'Mathematics'),(3,'Physics');
INSERT INTO student VALUES
 (1,'Ana Ruiz','ana@uni.example',1,3.80),
 (2,'Ben Cole','ben@uni.example',1,3.20),
 (3,'Cara Dunn','cara@uni.example',2,3.90),
 (4,'Dev Shah','dev@uni.example',2,2.80),
 (5,'Eli West','eli@uni.example',NULL,3.50);
INSERT INTO course VALUES ('C1','Databases'),('C2','Algorithms'),('C3','Calculus');
INSERT INTO enrolled VALUES (1,'C1','A'),(1,'C2','B'),(2,'C1','B'),(3,'C3','A'),(4,'C3','C'),(5,'C1','B');
