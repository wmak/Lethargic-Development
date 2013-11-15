#!/usr/bin/env python
# encoding: utf-8

from classes.models import Course, Department, CourseSchedule, Room
from datetime import datetime

def update_courses(items):
	for item in items:
		entry = Course.objects.filter(code=item["code"])
		if entry.count() == 0:
			add_course(item, True)

def update_schedule(items):
	for item in items:
		status = add_schedule(item, True)
		if not status:
			return status
	return "Successfully Updated"

def get_course(code):
	courses = Course.objects.filter(code=code)
	if courses:
		return courses[0]
	else:
		return None

def add_course(item, create_department = False):
	try:
		if create_department and Department.objects.filter(name = item["department"]).count() == 0:
			department = Department(name = item["department"], numberOfLecturers=0)
			department.save()
		elif (Department.objects.filter(name = item["department"]).count() == 1):
			department = Department.objects.get(name = item["department"])
		else:
			return "Error Department doesn't exist"
		course = Course(code=item["code"], name=item["name"], department=department)
		course.save()
		return course
	except Exception as e:
		print "EXCEPTION " + str(e)
		return e

def add_schedule(item, create_room = True, create_course = True):
	startTime = datetime.strptime(item["startTime"], "%H:%M")
	endTime = datetime.strptime(item["endTime"], "%H:%M")
	try:
		CourseSchedule(course=item["course"], room=item["room"], dayOfWeek=item['dayOfWeek'], enrolment = 0, startTime=startTime, endTime=endTime, typeOfSession=item["typeOfSession"]).save()
		if create_room and Room.objects.filter(code=item["room"]).count() == 0:
			Room(code = item["room"], capacity=0).save() 
		if create_course and Course.objects.filter(code=item["course"]).count() == 0:
			course = add_course({"code" : item["course"], "name" : "Default Name", "department" : "Default Department"}, create_department = True)
		elif Course.objects.filter(code=item["course"]).count() == 1:
			course = Course.objects.get(code=item["course"])
		else:
			return "Error: room doesn't exist"
		CourseSchedule(course=course, room=room, dayOfWeek=dayOfWeek, startTime=startTime, endTime=endTime, typeOfSession=item["typeOfSession"], enrolment = 0).save()
		return True
	except Exception as e:
		print "EXCEPTION " + str(e)
		return e