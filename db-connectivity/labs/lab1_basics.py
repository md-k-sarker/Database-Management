import sqlite3

DB = "school.db"          # a file in the current folder; use ":memory:" for a throwaway database

# ---- 1. Connect --------------------------------------------------------------
conn = sqlite3.connect(DB)            # creates the file if it does not exist
conn.execute("PRAGMA foreign_keys = ON")

# ---- 2. Create and load (a "with conn" block commits on success, rolls back on error) ----
with conn:
    conn.execute("DROP TABLE IF EXISTS student")
    conn.execute("""
        CREATE TABLE student (
            sid   INTEGER PRIMARY KEY,
            name  TEXT NOT NULL,
            major TEXT,
            gpa   REAL,
            phone TEXT
        )""")
    conn.executemany("INSERT INTO student VALUES (?, ?, ?, ?, ?)", [
        (1, "Ada Lovelace", "Computer Science", 3.9, "555-0101"),
        (2, "Ben Carter",   "Mathematics",      3.4, None),
        (3, "Carla Diaz",   "Computer Science", 3.7, "555-0103"),
        (4, "Dev Patel",    "Data Science",     3.2, None),
    ])

# ---- 3. Query and walk the result set ----------------------------------------
cur = conn.execute(
    "SELECT sid, name, gpa FROM student WHERE major = ? ORDER BY sid", ("Computer Science",))
print("columns:", [d[0] for d in cur.description])
for row in cur:                        # a cursor is iterable: one tuple per row
    print(row)

cur = conn.execute("SELECT sid, name FROM student ORDER BY sid")
print("fetchone:", cur.fetchone())             # the next single row
print("fetchall:", cur.fetchall())             # every remaining row, as a list
print("fetchone again:", cur.fetchone())       # None once the rows are used up

# ---- 4. Access columns by name, and meet NULL --------------------------------
conn.row_factory = sqlite3.Row
for row in conn.execute("SELECT name, phone FROM student ORDER BY sid"):
    print(row["name"], "->", row["phone"])    # a NULL value arrives as None
conn.row_factory = None

# ---- 5. One value, and how many rows an UPDATE changed -----------------------
print("students:", conn.execute("SELECT COUNT(*) FROM student").fetchone()[0])
with conn:
    cur = conn.execute("UPDATE student SET gpa = gpa + 0.1 WHERE major = ?", ("Data Science",))
    print("rows updated:", cur.rowcount)

# ---- 6. Transactions: nothing is permanent until commit ----------------------
conn.execute("INSERT INTO student VALUES (5, 'Eve Stone', 'Mathematics', 3.5, NULL)")
other = sqlite3.connect(DB)            # a second connection, like a second user
print("before commit, the other user sees:", other.execute("SELECT COUNT(*) FROM student").fetchone()[0])
other.close()
conn.commit()
other = sqlite3.connect(DB)
print("after commit, the other user sees:", other.execute("SELECT COUNT(*) FROM student").fetchone()[0])
other.close()

# ---- 7. A failed transaction is undone ---------------------------------------
try:
    with conn:
        conn.execute("INSERT INTO student VALUES (6, 'Fay Wu', 'Data Science', 3.8, NULL)")
        conn.execute("INSERT INTO student VALUES (1, 'Duplicate', 'None', 0.0, NULL)")   # sid 1 already exists
except sqlite3.IntegrityError as e:
    print("error:", e)
print("students after the failed block:", conn.execute("SELECT COUNT(*) FROM student").fetchone()[0])

conn.close()                           # always release the connection when you are done
