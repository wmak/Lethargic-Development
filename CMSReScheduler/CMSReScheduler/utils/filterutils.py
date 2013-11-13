import time
import datetime
from classes.models import CourseSchedule
from classes.models import Course
from classes.models import Room

def handleLength(qSet, dt):
	for r in qSet:
		csSet = CourseSchedule.filter(room = r.code)
		for cs in csSet:
			if cs.starTime < dt.hour:
				hOffset = cs.getLength() / 60
				mOffset = cs.getLength() % 60
				if cs.starTime.hour + hOffset > dt.hour:
					qSet.remove(r)
					break
				elif cs.starTime.hour + hOffset == dt.hour:
					if cs.starTime.minute + mOffset > 60:
						qSet.remove(r)
						break
	return qSet

def checkLengthOfAvailability(qSet, length):
	for r in qSet:
		csSet = CourseSchedule.filter(room = r.code).orderby(dayOfWeek, starTime)
		available = false
		for i in range (0, csSet.length):
			if i + 1 == csSet.length:
				break
			elif csSet[i].dayOfWeek != csSet[i+1].dayOfWeek
				continue
			#Calculating endTime for csSet[i]
			endTime = csSet[i].starTime.hour * 60 + csSet[i].starTime.minute + csSet[i].getLength()
			#Calculating startTime in minutes for csSet[i+1]
			sTime = csSet[i+1].starTime.hour * 60 + csSet[i+1].starTime.minute
			if sTime - endTime > length:
				available = true
		if available == false
			qSet.remove(r)
		available = false
	return qSet 


#For Rooms we are considering the following fields:
# - capacity: an integer indicating the minimum capacity the room should have
# - availableon: the day to use checking if the room is available
# - availableat: the startTime to use when checking if the room is available
# - availablefor: the length to use when checking if the room is available
# - building: two characters indicating the code for a building (IC, for example)
def filterRooms(body):
    qSet = Room.objects.all()
    if body.has_key("capacity"):
    	if body["capacity"]:
    		qSet = qSet.filter(capacity__gt = body["capacity"])
    if body.has_key("building"):
    	if body["building"]:
    		qSet = qSet.filter(code__startswith = body["building"])
    if body.has_key("availableon"):
    	if body["availableon"]:
			qSet = qSet.filter(courseschedule__dayOfWeek = vList[i])
	if body.has_key("availableat"):
		if body["availableat"]:
			t = time.strptime(body["availableat"], "%H:%M")
			dt = datetime.time(t.tm_hour, t.tm_min)
			qSet = qSet.exclude(courseschedule__startTime = dt)
			qSet = handleLength(qSet, dt)
	if body.has_key("availablefor"):
		if body["availablefor"]:
			qSet = checkLengthOfAvailability(qSet, body["availablefor"])
	return qSet

#For Courses we are considering the following fields:
# - roomcode: will be used to return courses that have sessions in this room
# - starttime: will be used to return all the courses that have sessions that start at the given time
# - building: two characters indicating the code for a building (IC, for example).
#             Will be used to return courses that have session in that building. 
#The order of the fields does not matter as long as the values are 
#in the same order.
def filterCourses(body):
	qSet = Course.objects.all()
	if body.has_key("roomcode"):
		if body["roomcode"]:
    		qSet = qSet.exclude(courseschedule__room = body["roomcode"])
	if body.has_key("startTime"):
		if body["startTime"]:
			t = time.strptime(body["startTime"], "%H:%M")
			dt = datetime.time(t.tm_hour, t.tm_min)
			qSet = qSet.filter(courseschedule__startTime = dt)
	if body.has_key("building"):
		if body["building"]:
			qSet = qSet.filter(courseschedule__room__startswith = body["building"])
	return qSet

