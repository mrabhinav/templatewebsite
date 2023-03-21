import sqlite3


conn = sqlite3.connect("boats.db")
cur = conn.cursor()
newcapacity = 6
boatsid = 3
cur.execute("UPDATE boats SET capacity = ? WHERE boatid = ?;", [newcapacity, boatsid])