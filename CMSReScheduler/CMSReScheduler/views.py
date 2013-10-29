#!/usr/bin/env python
# encoding: utf-8

import utils.csvutils as csvutils

from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from forms import UploadCsv
import simplejson as json

from classes.models import Course


def home(request):
	return render(request, 'test.html')

def csvimport(request):
	if request.method == 'POST':
		form = UploadCsv(request.POST, request.FILES)
		# The format is hardcoded and following the database's structure
		# because we don't know how the csv file will be yet. 
		# FIX that when we do.
		format = ['code', 'name', 'enrolment', 'department']
		parsed = csvutils.parse(request.FILES['file'], format, ',')
		csvutils.update_courses(parsed)
		return HttpResponse('CSV file imported sucessfully.')
	else:
		form = UploadCsv()
	return render_to_response('csvimport.html', {'form': form}, context_instance=RequestContext(request))
	
def admin(request):
	return render(request, 'admin/index.html')

def admin_upload(request):
	return render(request, 'admin/upload.html')

@csrf_exempt
def course(request, course):
	''' 
		Perform an action on a course 
		PUT -- Modify the course
		GET -- All relevant information pertaining to this course
		DELETE -- Remove this course from the schedule (It will still exist as a course)
		POST -- Add a new course
	'''
	info = {"Error" : "Nothing happened somehow"}
	status = 500
	try:
		current = Course.objects.filter(code=course)
		if current.count() != 0:
			if request.method == "PUT":
				params = QueryDict(request.body, request.encoding)
				print params
			elif request.method == "GET":
				info = {"Name" : current[0].name, "Enrolment" : current[0].enrolment, "Department" : current[0].department.name}
				status = 200
			elif request.method == "DELETE":
				pass
			elif request.method == "POST":
				pass
			else:
				info = {"Error" : "Unknown request"}
				status = 400
		else:
			info = {"Error" : "Unknown course code"}
			status = 404
	except Exception as e:
		info = {"Error" : "Internal error occured" + e}
		status = 500
	data = json.dumps(info)
	return HttpResponse(content = data, status = status)
