def addUser(cursor,user,role):
	cursor.execute("INSERT INTO " + table + "(user, role) VALUES(?,?)", (user, role))

def addVenue(cursor,name,operating):
	cursor.execute("INSERT INTO " + table + "(name, operating) VALUES(?,?)", (name, operating))

def addEvent(cursor,name,venue,time):
	cursor.execute("INSERT INTO " + table + "(name, venue, time) VALUES(?,?,?)", (name, venue, time))
