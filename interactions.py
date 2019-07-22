from datetime import datetime, timedelta
from collections import namedtuple
import sqlite3

db = sqlite3.connect("database.db")
cursor = db.cursor()

# ---------------------------------- FUNCTIONS ------------------------------------- #
def findUser(name):
	cursor.execute(
		"""
		SELECT * FROM
			users
		WHERE
			user = ?
		""",
		(name,)
	)
	user = cursor.fetchone()
	if user:
		return user
	else:
		return None

def addUser(user, role):
	found = findUser(user)
	if found is None:
		cursor.execute(
			"""
			INSERT INTO
				users(user, role)
			VALUES(?, ?)
			""",
			(user, role)
		)
		db.commit()
		print("User " + user + " has been added successfully.")
	else:
		print("User not added. Username taken.")

def findVenue(name):
	cursor.execute(
		"""
		SELECT * FROM
			venues
		WHERE
			name = ?
		""",
		(name,)
	)
	venue = cursor.fetchone()
	if venue:
		return venue
	else:
		return None

def addVenue(name, open, close):
	found = findVenue(name)
	if found is None:
		cursor.execute(
			"""
			INSERT INTO 
				venues(name, open, close)
			VALUES(?, ?, ?)
			""",
			(name, open, close)
		)
		db.commit()
		print("Venue " + name + " has been added succesfully.")
	else:
		print("Failed to add venue. A venue with the same name already exists.")

def addEvent(name, venue, time):
	cursor.execute(
		"""
		INSERT INTO
			events(name, venue, time)
		VALUES(?,?,?)
		""",
		(name, venue, time)
	)

def getTimeslotsByVenue(venue, time):
	timeslots = searchTimeslots(time)
	return timeslots.get(venue, [])

def getVenuesByTimeslot(time):
	timeslots = searchTimeslots(time)
	time = roundHour(time)
	venues = []

	for venue in timeslots:
		if time in timeslots[venue]:
			venues.append(venue)
	
	return venues

def searchTimeslots(time):
	cursor.execute(
		"""
		SELECT
			v.*,
			GROUP_CONCAT(e.time) as reserved
		FROM venues v
			JOIN events e
			ON v.id = e.venue
		WHERE ? BETWEEN open AND close
		GROUP BY (v.id)
		""", (time,)
	)

	VenueRecord = namedtuple('VenueRecord','id, name, open, close, reserved')
	all = map(VenueRecord._make, cursor.fetchall())
	timeslots = {}

	for row in all:
		venue = row.name
		timeslots[venue] = []
		now = datetime.strptime(roundHour(time), "%H:%M:%S")
		close = datetime.strptime(row.close, "%H:%M:%S")
		diff = close.hour - now.hour
		
		i = 0
		while i < diff:
			slot = (now + timedelta(hours=i)).strftime("%H:%M:%S")
			if slot not in row.reserved.split(','):
				timeslots[venue].append(slot)
			i += 1
	
	return timeslots

def roundHour(time):
	dt = datetime.strptime(time, "%H:%M:%S")
	start = dt.replace(minute=0, second=0, microsecond=0)
	half_hour = dt.replace(minute=30, second=0, microsecond=0)

	dt = start + timedelta(hours=1) if dt >= half_hour else start
	return dt.strftime("%H:%M:%S")
