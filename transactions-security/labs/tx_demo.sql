-- Transactions and security demo database for COSC 431 Module 10 (illustrative data)
-- Run in MySQL 8.4. Drops and recreates the database tx_demo.
DROP DATABASE IF EXISTS tx_demo;
CREATE DATABASE tx_demo;
USE tx_demo;

CREATE TABLE account (
  id      INT PRIMARY KEY,
  owner   VARCHAR(20) NOT NULL,
  balance INT NOT NULL,
  CONSTRAINT balance_not_negative CHECK (balance >= 0)
) ENGINE=InnoDB;

CREATE TABLE orders (
  id       INT PRIMARY KEY,
  customer VARCHAR(20) NOT NULL,
  amount   INT NOT NULL,
  INDEX idx_amount (amount)
) ENGINE=InnoDB;

CREATE TABLE customers (
  id    INT PRIMARY KEY,
  name  VARCHAR(30) NOT NULL,
  email VARCHAR(40) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE employees (
  id     INT PRIMARY KEY,
  name   VARCHAR(30) NOT NULL,
  salary INT NOT NULL
) ENGINE=InnoDB;

INSERT INTO account VALUES (1,'Alice',1000),(2,'Bob',1000);
INSERT INTO orders VALUES (1,'Alice',50),(2,'Bob',150),(3,'Alice',250);
INSERT INTO customers VALUES (1,'Alice','alice@example.com'),(2,'Bob','bob@example.com');
INSERT INTO employees VALUES (1,'Dana',70000),(2,'Eli',65000);
