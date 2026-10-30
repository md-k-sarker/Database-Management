-- Fundamentals demo database for COSC 431 Module 1 (illustrative data, made up for teaching)
-- Run in MySQL 8.4. Drops and recreates the database m1_demo.
DROP DATABASE IF EXISTS m1_demo;
CREATE DATABASE m1_demo;
USE m1_demo;

CREATE TABLE customer (
  customer_id INT PRIMARY KEY,
  name  VARCHAR(30) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  city  VARCHAR(20) NOT NULL
);
CREATE TABLE purchase (
  purchase_id INT PRIMARY KEY,
  customer_id INT NOT NULL,
  item  VARCHAR(30) NOT NULL,
  qty   INT NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);
INSERT INTO customer VALUES (1,'Ana','555-0101','Muncie'),(2,'Ben','555-0102','Indianapolis'),(3,'Cara','555-0103','Muncie'),(4,'Dev','555-0104','Fort Wayne');
INSERT INTO purchase VALUES (1,1,'Notebook',3),(2,1,'Pencil',10),(3,2,'Stapler',1),(4,3,'Notebook',2),(5,3,'Marker',4),(6,4,'Pencil',6);

-- One view per "department" application
CREATE VIEW v_sales   AS SELECT customer_id, name, phone FROM customer;
CREATE VIEW v_billing AS SELECT customer_id, name, phone FROM customer;
CREATE VIEW v_support AS SELECT customer_id, name, phone FROM customer;
