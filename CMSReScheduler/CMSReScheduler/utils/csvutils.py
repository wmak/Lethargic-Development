#!/bin/python

import csv

def parse(filename, format):
	items = []
	with open(filename, 'rb') as csvfile:
		parser = csv.reader(csvfile, delimiter=',')
		for row in parser:
			new_item = {}
			for i in range(len(format)):
				new_item[format[i]] = row[i]
			items.append(new_item)
	return items
