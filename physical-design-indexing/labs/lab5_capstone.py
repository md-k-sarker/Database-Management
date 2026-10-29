"""Capstone: choose indexes for a workload, then let the database grade your choice.

Edit PROPOSED below (one CREATE INDEX statement per entry), run the file, and read the report.
"""
import random
import sqlite3
import time

# ---------------------------------------------------------------- YOUR ANSWER
PROPOSED = [
    # "CREATE INDEX idx_example ON orders (status)",
]
# -----------------------------------------------------------------------------

random.seed(11)
conn = sqlite3.connect(":memory:")
conn.executescript("""
CREATE TABLE customers   (customer_id INTEGER PRIMARY KEY, email TEXT NOT NULL, name TEXT NOT NULL, city TEXT);
CREATE TABLE orders      (order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL,
                          status TEXT NOT NULL, total REAL NOT NULL, created TEXT NOT NULL);
CREATE TABLE order_items (item_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL,
                          product_id INTEGER NOT NULL, qty INTEGER NOT NULL);
""")
NC, NO = 20_000, 100_000
cities = ["Bowie", "Laurel", "Largo", "Upper Marlboro", "Greenbelt", "Hyattsville"]
conn.executemany("INSERT INTO customers VALUES (?,?,?,?)",
                 [(i, f"user{i}@example.com", f"Customer {i}", random.choice(cities)) for i in range(1, NC + 1)])
status_pool = ["paid"] * 6 + ["shipped"] * 3 + ["returned"]
conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?)",
                 [(i, random.randint(1, NC), random.choice(status_pool), round(random.uniform(5, 500), 2),
                   f"2026-{random.randint(1, 10):02d}-{random.randint(1, 28):02d}") for i in range(1, NO + 1)])
conn.executemany("INSERT INTO order_items (order_id, product_id, qty) VALUES (?,?,?)",
                 [(random.randint(1, NO), random.randint(1, 500), random.randint(1, 5)) for _ in range(300_000)])
conn.commit()

for stmt in PROPOSED:
    conn.execute(stmt)
conn.execute("ANALYZE")

# The reads of the workload: (name, how often per 1,000 operations, SQL, parameter factory).
# The other 200 operations per 1,000 are writes: placing a new order with its items (timed at the end).
WORKLOAD = [
    ("W1 customer's 10 newest orders", 300,
     "SELECT order_id, created, total FROM orders WHERE customer_id = ? ORDER BY created DESC LIMIT 10",
     lambda: (random.randint(1, NC),)),
    ("W2 login by email", 200,
     "SELECT customer_id, name FROM customers WHERE email = ?",
     lambda: (f"user{random.randint(1, NC)}@example.com",)),
    ("W3 items of one order", 250,
     "SELECT product_id, qty FROM order_items WHERE order_id = ?",
     lambda: (random.randint(1, NO),)),
    ("W4 ops: shipped orders in a week", 40,
     "SELECT order_id, total FROM orders WHERE status = 'shipped' AND created BETWEEN ? AND ?",
     lambda: ("2026-05-01", "2026-05-07")),
    ("W5 revenue since a date (paid)", 10,
     "SELECT SUM(total) FROM orders WHERE status = 'paid' AND created >= ?",
     lambda: ("2026-09-15",)),
]


def plan(sql, params):
    return " | ".join(r[3] for r in conn.execute("EXPLAIN QUERY PLAN " + sql, params))


def avg_ms(sql, make_params, runs):
    t0 = time.perf_counter()
    for _ in range(runs):
        conn.execute(sql, make_params()).fetchall()
    return (time.perf_counter() - t0) * 1000 / runs


print("indexes proposed:", PROPOSED or "none")
print(f"\n{'query':<36}{'avg ms':>9}   plan")
weighted = 0.0
for name, per1000, sql, mk in WORKLOAD:
    runs = 30 if "SCAN" in plan(sql, mk()) else 300
    ms = avg_ms(sql, mk, runs)
    weighted += ms * per1000 / 1000
    print(f"{name:<36}{ms:>9.3f}   {plan(sql, mk())}")
print(f"\nweighted average read cost per operation: {weighted:.3f} ms  (weighted by how often each query runs)")

# the write side of the workload: new orders and their items
t0 = time.perf_counter()
conn.executemany("INSERT INTO orders (customer_id, status, total, created) VALUES (?,?,?,?)",
                 [(random.randint(1, NC), "paid", 20.0, "2026-10-01") for _ in range(20_000)])
conn.executemany("INSERT INTO order_items (order_id, product_id, qty) VALUES (?,?,?)",
                 [(random.randint(1, NO), random.randint(1, 500), 1) for _ in range(40_000)])
conn.commit()
print(f"writes: 60,000 inserts took {(time.perf_counter() - t0) * 1000:.0f} ms")
