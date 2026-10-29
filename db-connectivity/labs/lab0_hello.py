import sqlite3

# 1. Connect. SQLite needs no server: ":memory:" is a database that lives inside this program.
conn = sqlite3.connect(":memory:")
print("connected, SQLite version", sqlite3.sqlite_version)

# 2. Get a cursor, the object that sends statements and holds results.
cur = conn.cursor()

# 3. Execute statements.
cur.execute("CREATE TABLE greeting (id INTEGER PRIMARY KEY, text TEXT)")
cur.execute("INSERT INTO greeting (text) VALUES (?)", ("Hello, database!",))
conn.commit()

# 4. Process the result.
cur.execute("SELECT id, text FROM greeting")
print(cur.fetchone())

# 5. Close what you opened.
cur.close()
conn.close()
print("closed")
