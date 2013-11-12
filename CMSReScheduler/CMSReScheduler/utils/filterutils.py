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
				hOffset = cs.length / 60
				mOffset = cs.length % 60
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
			endTime = csSet[i].starTime.hour * 60 + csSet[i].starTime.minute + csSet[i].length
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
def filterRooms(fList, vList):
    qSet = Room.objects.all()
    for i in range (0, fList.length):
        if fList[i] == 'capacity':
            qSet = qSet.filter(capacity__gt = int(vList[i]))
        elif fList[i] == 'building':
            qSet = qSet.filter(code__startswith = vList[i])
        elif fList[i] == 'availableon':
            qSet = qSet.filter(courseschedule__dayOfWeek = vList[i])
        elif fList[i] == 'availableat':
            t = time.strptime(vList[i], "%H:%M")
            dt = datetime.time(t.tm_hour, t.tm_min)
            qSet = qSet.exclude(courseschedule__startTime = dt)
            qSet = handleLength(qSet, dt);
        elif fList[i] == 'availablefor':
            qSet = checkLengthOfAvailability(qSet, int(vList[i]))
    return qSet



#For Courses we are considering the following fields:
# - roomcode: will be used to return courses that have sessions in this room
# - starttime: will be used to return all the courses that have sessions that start at the given time
# - building: two characters indicating the code for a building (IC, for example).
#             Will be used to return courses that have session in that building. 
#The strings must be separated by '-'s.
#The order of the fields does not matter as long as the values are 
#in the same order.
def filterCourses(fList, vList):
    qSet = Course.objects.all()
    for i in range (0, fList.length):
        if fList[i] == "roomcode":
            qSet = qSet.exclude(courseschedule__room__code = vList[i])
        elif fList[i] == "starttime":
            t = time.strptime(vList[i], "%H:%M")
            dt = datetime.time(t.tm_hour, t.tm_min)
            qSet = qSet.filter(courseschedule__startTime = dt)
        elif fList[i] == "building":
            qSet = qSet.filter(courseschedule__room__code__startswith = vList[i])
    return qSet

