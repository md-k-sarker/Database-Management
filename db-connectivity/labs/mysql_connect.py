# pip install mysql-connector-python
import os
import mysql.connector

conn = mysql.connector.connect(
    host="localhost", port=3306,
    user=os.environ.get("DB_USER", "app_user"),
    password=os.environ.get("DB_PASS", "change_me"),
    database="school",
)
try:
    cur = conn.cursor()
    # mysql.connector uses %s as the placeholder (it is NOT Python string formatting)
    cur.execute("SELECT sid, name, gpa FROM student WHERE major = %s AND gpa >= %s ORDER BY sid",
                ("Computer Science", 3.5))
    for sid, name, gpa in cur.fetchall():
        print(sid, name, gpa)

    cur.execute("UPDATE student SET gpa = %s WHERE sid = %s", (3.95, 1))
    print("rows updated:", cur.rowcount)
    conn.commit()                      # connectors for MySQL do not auto-commit by default
finally:
    conn.close()
