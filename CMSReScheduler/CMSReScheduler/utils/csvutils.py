#!/usr/bin/env python
# encoding: utf-8

import csv
from classesutils import add_course

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
	parser = csv.reader(csvfile, delimiter=delimiter)
	for row in parser:
		new_item = {}
		for i in range(len(format)):
			new_item[format[i]] = row[i].strip()
		items.append(new_item)
	return items

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

