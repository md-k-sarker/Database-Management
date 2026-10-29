import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE student (sid INTEGER PRIMARY KEY, name TEXT, major TEXT, gpa REAL, note TEXT)")
conn.executemany(
    "INSERT INTO student VALUES (:sid, :name, :major, :gpa, :note)",      # named style: a dict per row
    [
        {"sid": 1, "name": "Ada",   "major": "Computer Science", "gpa": 3.9, "note": "100% attendance"},
        {"sid": 2, "name": "Ben",   "major": "Mathematics",      "gpa": 3.4, "note": "1000 volunteer hours"},
        {"sid": 3, "name": "Carla", "major": "Computer Science", "gpa": 3.7, "note": None},
        {"sid": 4, "name": "Dev",   "major": "Data Science",     "gpa": 3.2, "note": None},
        {"sid": 5, "name": "Eve",   "major": "Mathematics",      "gpa": 3.5, "note": None},
    ],
)

# ---- 1. Named parameters ---------------------------------------------------------
rows = conn.execute(
    "SELECT name FROM student WHERE major = :major AND gpa >= :min_gpa ORDER BY sid",
    {"major": "Computer Science", "min_gpa": 3.7}).fetchall()
print("named:", rows)

# ---- 2. An IN (...) list: build the placeholders, never the values ---------------
ids = [1, 3, 5]
placeholders = ",".join("?" * len(ids))                    # "?,?,?"
sql = f"SELECT name FROM student WHERE sid IN ({placeholders}) ORDER BY sid"
print("IN:", sql, "->", conn.execute(sql, ids).fetchall())

# ---- 3. LIKE: a % or _ typed by the user still acts as a wildcard ----------------
def escape_like(text):
    return text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")

term = "100%"
naive = conn.execute("SELECT name FROM student WHERE note LIKE ?", (f"%{term}%",)).fetchall()
exact = conn.execute("SELECT name FROM student WHERE note LIKE ? ESCAPE '\\'",
                     (f"%{escape_like(term)}%",)).fetchall()
print("naive LIKE :", naive, " <- also matches '1000 volunteer hours'")
print("escaped LIKE:", exact)

# ---- 4. Optional filters: append fixed fragments, collect values separately ------
def search(major=None, min_gpa=None):
    conditions, params = [], []
    if major is not None:
        conditions.append("major = ?")
        params.append(major)
    if min_gpa is not None:
        conditions.append("gpa >= ?")
        params.append(min_gpa)
    where = (" WHERE " + " AND ".join(conditions)) if conditions else ""
    return conn.execute("SELECT name FROM student" + where + " ORDER BY sid", params).fetchall()

print("no filters   :", search())
print("major only   :", search(major="Mathematics"))
print("both filters :", search(major="Mathematics", min_gpa=3.5))

# ---- 5. Bulk update: executemany -------------------------------------------------
cur = conn.executemany("UPDATE student SET note = ? WHERE sid = ?",
                       [("dean's list", 1), ("dean's list", 3)])
print("rows changed by executemany:", cur.rowcount)

# ---- 6. Three mistakes you will meet, and their real error messages --------------
mistakes = [
    ("single value not in a tuple",
     lambda: conn.execute("SELECT * FROM student WHERE major = ?", "Computer Science")),
    ("too few values",
     lambda: conn.execute("SELECT * FROM student WHERE major = ? AND gpa > ?", ("Mathematics",))),
    ("wrong table name",
     lambda: conn.execute("SELECT * FROM students")),
]
for label, attempt in mistakes:
    try:
        attempt()
    except sqlite3.Error as e:
        print(f"{label}: {type(e).__name__}: {e}")
print("the fix for the first one: pass a tuple with a trailing comma, e.g. (major,)")
