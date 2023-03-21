import sqlite3

conn = sqlite3.connect("boats.db")
cur = conn.cursor()
# cur.execute("""CREATE TABLE user
# (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, email TEXT, password text);""")

# cur.execute("""CREATE TABLE boats
# (boatid INTEGER PRIMARY KEY AUTOINCREMENT, boatname TEXT, boatcompany TEXT, departurecity TEXT, destination TEXT, capacity INTEGER)""")

# cur.execute("""INSERT INTO boats(boatname, boatcompany, departurecity,
#             destination, capacity) values (?,?,?,?,?);""", ("Serendipity", "WaterWays", "Miami", "Baltimore", 10))

# cur.execute("""CREATE TABLE resumeparser
# (ticketid INTEGER PRIMARY KEY AUTOINCREMENT, boatname TEXT, boatcompany TEXT, 
# departurecity TEXT, destination TEXT, seats INTEGER, timebooked TEXT, datebooked TEXT, 
# timeof TEXT, dateof TEXT)""")
# cur.execute("""INSERT INTO resumeparser(boatname, boatcompany, destination) values (?,?,?);""", ("name", "email", "phonenumberasdfaswdfaw"))
# x = cur.execute("SELECT * FROM resumeparser").fetchall()
# print (x)


# boat = cur.execute ("SELECT * FROM boats").fetchall()
# print(boat)
conn.commit()
conn.close()


# cur.execute ("DROP TABLE user;")

# print("Created")