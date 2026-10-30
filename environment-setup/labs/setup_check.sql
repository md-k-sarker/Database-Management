-- COSC 431 Module 0: environment check (MySQL 8.4)
SELECT VERSION();
SHOW DATABASES;
CREATE DATABASE setup_check;
USE setup_check;
CREATE TABLE hello (id INT PRIMARY KEY, message VARCHAR(40));
INSERT INTO hello VALUES (1, 'My MySQL server works');
SELECT * FROM hello;
SHOW DATABASES;
DROP DATABASE setup_check;
