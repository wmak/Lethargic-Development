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
		department = Department.objects.get(name = item["department"])
		course = Course(code=item["code"], name=item["name"], enrolment=item["enrolment"], department=department)
		course.save()
		return course
	except Exception as e:
		if create_department:
			Department(name = item["department"], numberOfLecturers=0).save()
			department = Department.objects.get(name = item["department"])
			course = Course(code=item["code"], name=item["name"], enrolment=item["enrolment"], department=department)
			course.save()
			return course
		else:
			return e

def add_schedule(item, create_room = True, create_course = True):
	startTime = datetime.strptime(item["startTime"], "%H:%M")
	endTime = datetime.strptime(item["endTime"], "%H:%M")
	room = None
	course = None
	dayOfWeek = item['dayOfWeek']
	try:
		if create_room and Room.objects.filter(code=item["room"]).count() == 0:
			room = Room(code = item["room"], capacity=0)
			room.save() 
		elif (Room.objects.filter(code=item["room"]).count() == 1):
			room = Room.objects.get(code = item["room"])
		else:
			return "Error: room doesn't exist"
		if create_course and Course.objects.filter(code=item["course"]).count() == 0:
			course = add_course({"code" : item["course"], "name" : "Default Name", "enrolment" : 0, "department" : "Default Department"}, create_department = True)
		elif Course.objects.filter(code=item["course"]).count() == 1:
			course = Course.objects.get(code=item["course"])
		else:
			return "Error: room doesn't exist"
		CourseSchedule(course=course, room=room, dayOfWeek=dayOfWeek, startTime=startTime, endTime=endTime, typeOfSession=item["typeOfSession"]).save()
	except Exception as e:
		print "EXCEPTION" + str(e)
		return e