import random
import sqlite3
import time

random.seed(1)
conn = sqlite3.connect(":memory:")
conn.execute("""CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    status      TEXT    NOT NULL,
    amount      REAL    NOT NULL,
    created     TEXT    NOT NULL)""")

N = 200_000
statuses = ["paid", "shipped", "returned"]
rows = [(random.randint(1, 20_000), random.choice(statuses), round(random.uniform(5, 500), 2),
         f"2026-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}") for _ in range(N)]
conn.executemany("INSERT INTO orders (customer_id, status, amount, created) VALUES (?, ?, ?, ?)", rows)
conn.commit()


def best_ms(sql, params=(), repeat=5):
    """Best of several runs, in milliseconds (best-of reduces noise from other programs)."""
    best = None
    for _ in range(repeat):
        t0 = time.perf_counter()
        conn.execute(sql, params).fetchall()
        dt = (time.perf_counter() - t0) * 1000
        best = dt if best is None or dt < best else best
    return best


def plan(sql, params=()):
    return " | ".join(r[3] for r in conn.execute("EXPLAIN QUERY PLAN " + sql, params))


def size_kb():
    return conn.execute("PRAGMA page_count").fetchone()[0] * conn.execute("PRAGMA page_size").fetchone()[0] // 1024


Q_EQ = "SELECT order_id, amount FROM orders WHERE customer_id = ?"
Q_RANGE = "SELECT order_id FROM orders WHERE created BETWEEN '2026-03-01' AND '2026-03-07'"

print(f"SQLite {sqlite3.sqlite_version}; {N:,} rows; table size {size_kb():,} KB\n")

print("--- before any index ---")
before_eq, before_rg = best_ms(Q_EQ, (4242,)), best_ms(Q_RANGE)
print("equality :", plan(Q_EQ, (4242,)), f"-> {before_eq:.2f} ms")
print("range    :", plan(Q_RANGE), f"-> {before_rg:.2f} ms")

conn.execute("CREATE INDEX idx_orders_customer ON orders (customer_id)")
conn.execute("CREATE INDEX idx_orders_created ON orders (created)")
print("\n--- after CREATE INDEX on customer_id and on created ---")
after_eq, after_rg = best_ms(Q_EQ, (4242,)), best_ms(Q_RANGE)
print("equality :", plan(Q_EQ, (4242,)), f"-> {after_eq:.3f} ms  ({before_eq / after_eq:,.0f}x faster)")
print("range    :", plan(Q_RANGE), f"-> {after_rg:.2f} ms  ({before_rg / after_rg:,.1f}x faster)")
print(f"table + indexes now take {size_kb():,} KB")

print("\n--- the price: writes get slower ---")
batch = [(random.randint(1, 20_000), "paid", 10.0, "2026-06-15") for _ in range(20_000)]


def insert_ms():
    t0 = time.perf_counter()
    conn.executemany("INSERT INTO orders (customer_id, status, amount, created) VALUES (?, ?, ?, ?)", batch)
    conn.commit()
    return (time.perf_counter() - t0) * 1000


with_idx = insert_ms()
conn.execute("DROP INDEX idx_orders_customer")
conn.execute("DROP INDEX idx_orders_created")
without_idx = insert_ms()
print(f"insert 20,000 rows with 2 indexes   : {with_idx:6.0f} ms")
print(f"insert 20,000 rows with no indexes  : {without_idx:6.0f} ms")
print(f"each index adds work to every write ({with_idx / without_idx:.1f}x slower here)")
print("\nNote: timings change from run to run and machine to machine. The plans and the ratios' direction do not.")
