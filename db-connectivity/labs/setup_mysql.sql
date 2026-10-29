-- Run once as a MySQL administrator (for example:  mysql -u root -p < setup_mysql.sql)
CREATE DATABASE IF NOT EXISTS school;
USE school;

DROP TABLE IF EXISTS student;
CREATE TABLE student (
  sid   INT PRIMARY KEY,
  name  VARCHAR(60) NOT NULL,
  major VARCHAR(40),
  gpa   DECIMAL(3,2),
  phone VARCHAR(20)
);
INSERT INTO student VALUES
  (1, 'Ada Lovelace', 'Computer Science', 3.90, '555-0101'),
  (2, 'Ben Carter',   'Mathematics',      3.40, NULL),
  (3, 'Carla Diaz',   'Computer Science', 3.70, '555-0103'),
  (4, 'Dev Patel',    'Data Science',     3.20, NULL);

-- An account for the application: only what it needs, only on this database.
CREATE USER IF NOT EXISTS 'app_user'@'localhost' IDENTIFIED BY 'change_me';
GRANT SELECT, INSERT, UPDATE ON school.student TO 'app_user'@'localhost';
