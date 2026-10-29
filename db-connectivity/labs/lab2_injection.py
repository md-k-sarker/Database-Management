import sqlite3

conn = sqlite3.connect(":memory:")
conn.executescript("""
    CREATE TABLE users    (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT);
    CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL);
    INSERT INTO users VALUES (1, 'alice', 'alicepw', 'student'),
                             (2, 'bob',   'bobpw',   'student'),
                             (3, 'admin', 'S3cret!', 'admin');
    INSERT INTO products VALUES (1, 'Notebook', 4.00), (2, 'Pen', 1.50), (3, 'Stapler', 9.25);
""")   # (a real system stores password HASHES, never plain text; this is only a demo)


# ===================== Part 1: login =====================
def login_vulnerable(username, password):
    # DANGER: user input is pasted into the SQL text
    sql = f"SELECT username, role FROM users WHERE username = '{username}' AND password = '{password}'"
    print("   SQL sent  :", sql)
    try:
        return conn.execute(sql).fetchone()
    except sqlite3.Error as e:
        return f"ERROR: {e}"


def login_safe(username, password):
    # SAFE: the SQL text is fixed; the values travel separately as parameters
    sql = "SELECT username, role FROM users WHERE username = ? AND password = ?"
    return conn.execute(sql, (username, password)).fetchone()


attempts = [
    ("alice", "alicepw"),             # a normal, correct login
    ("alice", "wrong"),               # a normal, wrong password
    ("' OR '1'='1' --", "anything"),  # ATTACK: always-true condition, the rest commented out
    ("admin'--", ""),                 # ATTACK: log in as admin with no password
    ("O'Brien", "pw"),                # NOT an attack: an honest name containing an apostrophe
]
for u, p in attempts:
    print(f"username={u!r} password={p!r}")
    print("   vulnerable:", login_vulnerable(u, p))
    print("   safe      :", login_safe(u, p))


# ===================== Part 2: search (data theft with UNION) =====================
def search_vulnerable(term):
    sql = f"SELECT name, price FROM products WHERE name LIKE '%{term}%'"
    print("   SQL sent  :", sql)
    try:
        return conn.execute(sql).fetchall()
    except sqlite3.Error as e:
        return f"ERROR: {e}"


def search_safe(term):
    return conn.execute("SELECT name, price FROM products WHERE name LIKE ?", (f"%{term}%",)).fetchall()


print()
for term in ["pen",
             "%' UNION SELECT username, password FROM users --",
             "'; DROP TABLE users; --"]:
    print(f"search term={term!r}")
    print("   vulnerable:", search_vulnerable(term))
    print("   safe      :", search_safe(term))
print("users table still exists:", conn.execute("SELECT COUNT(*) FROM users").fetchone()[0], "rows")


# ===================== Part 3: what a placeholder cannot do =====================
ALLOWED_SORT = {"name", "price"}


def list_products(sort_by):
    # A ? placeholder holds a VALUE, never a column or table name. For those, check against a fixed list.
    if sort_by not in ALLOWED_SORT:
        return f"rejected: {sort_by!r}"
    return conn.execute(f"SELECT name, price FROM products ORDER BY {sort_by}").fetchall()


print()
print(list_products("price"))
print(list_products("price; DROP TABLE users"))
