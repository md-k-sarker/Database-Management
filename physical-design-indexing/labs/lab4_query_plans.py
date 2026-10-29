import sqlite3

conn = sqlite3.connect(":memory:")
print("SQLite", sqlite3.sqlite_version, "\n")
conn.executescript("""
CREATE TABLE t (id INTEGER PRIMARY KEY, a INT, b INT, c INT, d INT,
                name TEXT COLLATE NOCASE, email TEXT, created TEXT);
CREATE INDEX idx_abc   ON t (a, b, c);
CREATE INDEX idx_name  ON t (name);
CREATE INDEX idx_email ON t (email);
CREATE INDEX idx_d     ON t (d);
""")
conn.executemany("INSERT INTO t (a, b, c, d, name, email, created) VALUES (?,?,?,?,?,?,?)",
                 [(i % 50, i % 7, i % 13, i, f"user{i}", f"u{i}@example.com", "2026-01-01") for i in range(5000)])


def show(title, sql):
    steps = [r[3] for r in conn.execute("EXPLAIN QUERY PLAN " + sql)]
    print(f"{title}\n    {sql}\n    -> " + "\n       ".join(steps) + "\n")


print("=== 1. Can the query use the index at all? ===\n")
show("equality on an indexed column", "SELECT * FROM t WHERE d = 100")
show("range on an indexed column", "SELECT * FROM t WHERE d BETWEEN 100 AND 200")
show("no index on this column", "SELECT * FROM t WHERE created = '2026-01-01'")
show("function wrapped around the column", "SELECT * FROM t WHERE d + 0 = 100")
show("inequality (!=) matches almost every row", "SELECT * FROM t WHERE d != 100")

print("=== 2. LIKE: the wildcard position decides ===\n")
show("prefix pattern", "SELECT * FROM t WHERE name LIKE 'user12%'")
show("leading wildcard", "SELECT * FROM t WHERE name LIKE '%12'")

print("=== 3. Composite index (a, b, c): column order matters ===\n")
show("a only (leftmost column)", "SELECT id FROM t WHERE a = 5")
show("a and b", "SELECT id FROM t WHERE a = 5 AND b = 3")
show("a, b and c", "SELECT id FROM t WHERE a = 5 AND b = 3 AND c = 2")
show("a and c (b skipped)", "SELECT id FROM t WHERE a = 5 AND c = 2")
show("range on b, then c after it", "SELECT id FROM t WHERE a = 5 AND b > 2 AND c = 2")
show("b only (leftmost column missing), selecting a column the index lacks", "SELECT name FROM t WHERE b = 3")
show("b only, but every column the query needs is in the index", "SELECT id FROM t WHERE b = 3")

print("=== 3b. Statistics can change the plan ===\n")
conn.execute("ANALYZE")      # gather statistics, as a real database does regularly
print("(after ANALYZE the planner knows column a has only 50 distinct values)\n")
show("b only, after ANALYZE", "SELECT name FROM t WHERE b = 3")

print("=== 4. Covering index: the answer comes from the index alone ===\n")
show("selects columns that are all in the index", "SELECT a, b, c FROM t WHERE a = 5")
show("selects a column that is not in the index", "SELECT a, b, c, name FROM t WHERE a = 5")

print("=== 5. ORDER BY: an index can supply the order for free ===\n")
show("order by the next index column", "SELECT id FROM t WHERE a = 5 ORDER BY b")
show("order by a column the index cannot supply", "SELECT id FROM t WHERE a = 5 ORDER BY d")

print("=== 6. Expression index: index the expression you search on ===\n")
conn.execute("CREATE INDEX idx_lower_email ON t (lower(email))")
show("search on lower(email) with the expression index", "SELECT id FROM t WHERE lower(email) = 'u5@example.com'")
