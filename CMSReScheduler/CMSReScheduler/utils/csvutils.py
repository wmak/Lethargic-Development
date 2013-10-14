#!/usr/bin/env python
# encoding: utf-8

import csv

def parse(filename, format, delimiter=','):
	''' parser takes a filename and a supposed format for the file, 
	delimeter is preset but can also be modified as needed
	it then returns a list of dictionaries with keys representing the type of data
	and values of the data itself

	str filename
	list format
	str delimeter
	'''
	items = []
	with open(filename, 'rb') as csvfile:
		parser = csv.reader(csvfile, delimiter=delimiter)
		for row in parser:
			new_item = {}
			for i in range(len(format)):
				new_item[format[i]] = row[i]
			items.append(new_item)
	return items
