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
		add_schedule(item, True)

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
			room = Room.objects.get(code = item["room"])
		else:
			return "Error Department doesn't exist"
		course = Course(code=item["code"], name=item["name"], department=department)
		course.save()
		return course
	except Exception as e:
		print "EXCEPTION" + str(e)
		return e

def add_schedule(item, create_room = True, create_course = True):
	startTime = datetime.strptime(item["startTime"], "%H:%M")
	endTime = datetime.strptime(item["endTime"], "%H:%M")
	room = None
	course = None
	dayOfWeek = item['dayOfWeek']
	try:
		CourseSchedule(course=item["course"], room=item["room"], enrolment = 0, dayOfWeek=dayOfWeek, startTime=startTime, endTime=endTime, typeOfSession=item["typeOfSession"]).save()
	except Exception as e:
		print "EXCEPTION" + str(e)
		return e