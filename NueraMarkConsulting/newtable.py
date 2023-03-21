import sqlite3
from debugpy import connect

conn = sqlite3.connect("parse.db")
cur = conn.cursor()

# cur.execute("""CREATE TABLE resumeparse
# (resumeid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, emails TEXT, 
# phonenumbers TEXT)""")

# cur.execute("""INSERT INTO resumeparse(name, emails, phonenumbers) values (?,?,?);""", ("name", "email", "phonenumberasdfaswdfaw"))
x = cur.execute("SELECT * FROM resumeparse")
print (x)

conn.commit()
conn.commit()