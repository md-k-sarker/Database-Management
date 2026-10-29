# Reference answer: replace the empty PROPOSED list in lab5_capstone.py with this one.
PROPOSED = [
    "CREATE INDEX idx_orders_cust_created ON orders (customer_id, created)",      # W1: equality column, then the ORDER BY column
    "CREATE UNIQUE INDEX idx_customers_email ON customers (email)",                # W2: one row per email
    "CREATE INDEX idx_items_order ON order_items (order_id)",                      # W3: the join/foreign-key column
    "CREATE INDEX idx_orders_status_created ON orders (status, created)",          # W4, W5: equality column, then range column
]
