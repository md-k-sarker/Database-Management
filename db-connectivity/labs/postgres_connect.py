# pip install psycopg2-binary
import os
import psycopg2

conn = psycopg2.connect(host="localhost", port=5432, dbname="school",
                        user=os.environ["DB_USER"], password=os.environ["DB_PASS"])
try:
    with conn:                          # commits on success, rolls back on error (does NOT close)
        with conn.cursor() as cur:
            cur.execute("SELECT sid, name FROM student WHERE major = %s", ("Computer Science",))
            print(cur.fetchall())
finally:
    conn.close()
