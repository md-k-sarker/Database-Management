-- Relational algebra demo database for COSC 431 Module 3 (illustrative data, made up for teaching)
-- Run in MySQL 8.4. Drops and recreates the database ra_demo.
DROP DATABASE IF EXISTS ra_demo;
CREATE DATABASE ra_demo;
USE ra_demo;

CREATE TABLE Student (
  sid   INT PRIMARY KEY,
  sname VARCHAR(30) NOT NULL,
  major VARCHAR(10) NOT NULL,
  gpa   DECIMAL(3,2)
);
CREATE TABLE Course (
  cid     VARCHAR(4) PRIMARY KEY,
  title   VARCHAR(30) NOT NULL,
  credits INT NOT NULL,
  dept    VARCHAR(10) NOT NULL
);
CREATE TABLE Instructor (
  iid   INT PRIMARY KEY,
  iname VARCHAR(30) NOT NULL,
  dept  VARCHAR(10) NOT NULL
);
CREATE TABLE Enrolled (
  sid   INT,
  cid   VARCHAR(4),
  grade VARCHAR(2),
  PRIMARY KEY (sid, cid),
  FOREIGN KEY (sid) REFERENCES Student(sid),
  FOREIGN KEY (cid) REFERENCES Course(cid)
);

INSERT INTO Student VALUES
 (1,'Ana','CS',3.80),(2,'Ben','CS',3.20),(3,'Cara','MATH',3.90),(4,'Dan','MATH',2.80),
 (5,'Eli','DS',3.50),(6,'Fay','DS',NULL),(7,'Gus','CS',3.00);
INSERT INTO Course VALUES
 ('C1','Databases',3,'CS'),('C2','Algorithms',4,'CS'),('C3','Calculus',4,'MATH'),
 ('C4','Statistics',3,'MATH'),('C5','Machine Learning',3,'DS'),('C6','Ethics',2,'PHIL');
INSERT INTO Instructor VALUES
 (1,'Okafor','CS'),(2,'Tanaka','MATH'),(3,'Brooks','DS'),(4,'Romero','CS');
INSERT INTO Enrolled VALUES
 (1,'C1','A'),(1,'C2','B'),(1,'C3','A'),(1,'C5','B'),
 (2,'C1','B'),(2,'C2',NULL),
 (3,'C2','A'),(3,'C3','A'),(3,'C4','B'),
 (4,'C3','C'),(4,'C4','B'),
 (5,'C1','B'),(5,'C4','C'),(5,'C5','A'),
 (6,'C5','B');
