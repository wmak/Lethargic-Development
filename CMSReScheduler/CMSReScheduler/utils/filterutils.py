import datetime
from classes.models import CourseSchedule

def handleLength(qSet, dt):
	for r in qSet:
		csSet = CourseSchedule.filter(room = r)
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
		csSet = CourseSchedule.filter(room = r).orderby(dayOfWeek, starTime)
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

