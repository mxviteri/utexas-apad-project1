import sqlite3
db = sqlite3.connect("database.db")
cursor = db.cursor()




# ---------------------------------- FUNCTIONS ------------------------------------- #
def listRoles():
	cursor.execute("SELECT * FROM roles")

def addUser(user,role):
	cursor.execute("INSERT INTO users(user, role) VALUES(?,?)", (user, role))

def addVenue(name,operating):
	cursor.execute("INSERT INTO venues(name, operating) VALUES(?,?)", (name, operating))

def addEvent(name,venue,time):
	cursor.execute("INSERT INTO events(name, venue, time) VALUES(?,?,?)", (name, venue, time))