-- Indexes and query plans on MySQL and PostgreSQL.
-- Written from each product's documented syntax; NOT run in a real MySQL or PostgreSQL server.
-- The idea matches the SQLite labs: create an index, ask for the plan, check that the plan changed.

-- ---------------------------------------------------------------- schema (both)
CREATE TABLE customers (
  customer_id INT PRIMARY KEY,
  email       VARCHAR(100) NOT NULL,
  name        VARCHAR(100) NOT NULL,
  city        VARCHAR(50)
);
CREATE TABLE orders (
  order_id    INT PRIMARY KEY,
  customer_id INT NOT NULL,
  status      VARCHAR(10) NOT NULL,
  total       DECIMAL(10,2) NOT NULL,
  created     DATE NOT NULL
);

-- ---------------------------------------------------------------- create indexes (both)
CREATE INDEX idx_orders_cust_created ON orders (customer_id, created);
CREATE UNIQUE INDEX idx_customers_email ON customers (email);

-- ---------------------------------------------------------------- ask for the plan
-- MySQL:
EXPLAIN SELECT order_id, created, total
FROM orders WHERE customer_id = 42 ORDER BY created DESC LIMIT 10;
-- Look at the "key" column (which index) and "rows" (estimated rows examined).
-- MySQL 8.0.18+ can also run the query and show real timings:
EXPLAIN ANALYZE SELECT order_id FROM orders WHERE customer_id = 42;

-- PostgreSQL:
EXPLAIN (ANALYZE, BUFFERS)
SELECT order_id, created, total
FROM orders WHERE customer_id = 42 ORDER BY created DESC LIMIT 10;
-- Look for "Index Scan" or "Index Only Scan" versus "Seq Scan", and the "Buffers" line.

-- ---------------------------------------------------------------- statistics (refresh them after big loads)
-- MySQL:       ANALYZE TABLE orders;
-- PostgreSQL:  ANALYZE orders;

-- ---------------------------------------------------------------- list the indexes on a table
-- MySQL:       SHOW INDEX FROM orders;
-- PostgreSQL:  SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'orders';

-- ---------------------------------------------------------------- expression index (search on lower(email))
-- PostgreSQL:
CREATE INDEX idx_customers_lower_email ON customers (lower(email));
-- MySQL 8.0.13+ (note the extra parentheses around the expression):
-- CREATE INDEX idx_customers_lower_email ON customers ((lower(email)));

-- ---------------------------------------------------------------- covering index
-- PostgreSQL 11+ can carry extra columns that are not part of the search key:
CREATE INDEX idx_orders_status_created ON orders (status, created) INCLUDE (total);
-- MySQL has no INCLUDE clause; to cover the query, add the column to the key instead:
-- CREATE INDEX idx_orders_status_created ON orders (status, created, total);

-- ---------------------------------------------------------------- other index types (PostgreSQL)
-- CREATE INDEX idx_orders_created_brin ON orders USING brin (created);   -- tiny index for huge, naturally ordered tables
-- CREATE INDEX idx_customers_hash ON customers USING hash (email);       -- equality only

-- ---------------------------------------------------------------- remove an index
-- MySQL:       DROP INDEX idx_orders_cust_created ON orders;
-- PostgreSQL:  DROP INDEX idx_orders_cust_created;
