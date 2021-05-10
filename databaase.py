import sqlite3

conn = sqlite3.connect("manager.db")

c = conn.cursor()

c.execute("CREATE TABLE names (name text)")
c.execute("CREATE TABLE users (username text, password text)")

conn.commit()
conn.close()