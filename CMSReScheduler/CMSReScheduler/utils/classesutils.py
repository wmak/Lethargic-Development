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
		Course(code=item["code"], name=item["name"], enrolment=item["enrolment"], department=department).save()
	except Exception as e:
		if create_department:
			Department(name = item["department"], numberOfLecturers=0).save()
			department = Department.objects.get(name = item["department"])
			Course(code=item["code"], name=item["name"], enrolment=item["enrolment"], department=department).save()
		else:
			return e

def add_schedule(item, create_room = False):
	startTime = datetime.strptime(item["startTime"], "%H:%M")
	endTime = datetime.strptime(item["endTime"], "%H:%M")
	course = Course.objects.get(code=item["course"])
	try:
		room = Room.objects.get(code = item["room"])
		CourseSchedule(course=course, room=room, dayOfWeek=item["dayOfWeek"], startTime=startTime, endTime=endTime, typeOfSession=item["typeOfSession"]).save()
	except Exception as e:
		print e
		if create_room:
			room = Room(code = item["room"], capacity=0)
			room.save()
			CourseSchedule(course=course, room=room, dayOfWeek=item["dayOfWeek"], startTime=startTime, endTime=endTime, typeOfSession=item["typeOfSession"]).save()
		else:
			return e