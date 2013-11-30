#!/usr/bin/env python
# encoding: utf-8

import csv
from classesutils import add_course
import codecs
import datetime
from classes.models import CourseSchedule

def parse(csvfile, format, delimiter=','):
	''' parser takes a filename and a supposed format for the file, 
	delimiter is preset but can also be modified as needed
	it then returns a list of dictionaries with keys representing the type of data
	and values of the data itself

	str filename
	list format
	str delimiter
	'''
	items = []
	parser = csv.reader(codecs.EncodedFile(csvfile,"utf-8"), delimiter=delimiter)
	for row in parser:
		new_item = {}
		for i in range(len(format)):
			new_item[format[i]] = row[i].strip()
		items.append(new_item)
	return items

def set_weekday(day):
	if day == 0:
		return "MO"
	elif day == 1:
		return "TU"
	elif day == 2:
		return "WE"
	elif day == 3:
		return "TH"
	elif day == 4:
		return "FR"
	elif day == 5:
		return "SA"
	else:
		return "SU"

def parse_room_file(roomfile):
	items = []
	file = open(str(roomfile), 'r')
	capacity = int(file.readline())
	dayOfWeek = 6 #Sunday
	room = str(roomfile).split('.')[0]
	for line in file:
		tokens = line.split('/')
		if len(tokens) == 3:
			#date line
			dt = datetime.date(month = int(tokens[0]), day = int(tokens[1]), year = int(tokens[2]))
			dayOfWeek = dt.weekday()
		else:
			'''we're assuming the following format here
			   startTime-endTime CourseCode Section
			'''
			tokens = line.split(' ')
			times = tokens[0].split('-')
			times[1] = times[1].rstrip()
			stime = datetime.datetime.strptime(times[0], "%H:%M")
			etime = datetime.datetime.strptime(times[1], "%H:%M")
			course = ""
			section = ""
			if len(tokens) == 3:
				course = tokens[1]
				section = tokens[2].rstrip()
			cs = CourseSchedule(course = course, room = room, dayOfWeek = set_weekday(dayOfWeek), startTime = stime.time(), endTime = etime.time(), typeOfSession = section, enrolment = 0)
			items.append(cs)
	return capacity, items




def update_departments(items):
	from classes.models import Department
	for item in items:
		entry = Department.objects.filter(name=item["name"])
		if entry.count() == 0:
			Department(name=item["name"], numberOfLecturers=item["numberOfLecturers"]).save()

def update_rooms(items):
	from classes.models import Room
	for item in items:
		entry = Room.object.filter(code=item["code"])
		if entry.count() == 0:
			Room(code=item["code"], capacity=item["capacity"]).save()

