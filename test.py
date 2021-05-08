import sqlite3

con = sqlite3.connect('mydatabase.db')
c = con.cursor()
c.execute("INSERT INTO meow VALUES(?, ?, ?)",(1, "kotik_sem", 5))