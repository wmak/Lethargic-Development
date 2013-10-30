#!/usr/bin/env python
# encoding: utf-8

import utils.csvutils as csvutils
import utils.classesutils as classutils

from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from forms import UploadCsv
import simplejson as json

from classes.models import Course, Department


def home(request):
	return render(request, 'test.html')


def import_csv_file(request, type):
    ''' NOTE: for now I have a single url for this. I can send them  each to a certain page if you guys prefer.
    This is still very much up for debate. Let me know what you all think '''
    if type == 'schedule':
        form = UploadCsv(type, request.FILES)
        format = ['code', 'name', 'enrolment']
        parser_list = parse(request.FILES['file'], format, ',')
        update_courses(parser_list)
        return HttpResponse('The schedule file has been uploaded!')
    elif type == 'room':
        form = UploadCsv(type, request.FILES)
        format = ['code', 'name', 'building']
        parser_list = parse(request.FILES['file'], format, ',')
        update_rooms(parser_list)
        return HttpResponse('Room file has been uploaded!')
    elif type == 'department':
        form = UploadCsv(type, request.FILES)
        format = ['code', 'name']
        parser_list = parse(request.FILES['file'], format, ',')
        update_departments(parser_list)
        return HttpResponse('Department file has been uploaded!')
    else:
        return HttpResponse('Invalid Type!')

def csvimport(request):
	if request.method == 'POST':
		form = UploadCsv(request.POST, request.FILES)
		# The format is hardcoded and following the database's structure
		# because we don't know how the csv file will be yet. 
		# FIX that when we do.
		format = ['code', 'name', 'enrolment', 'department']
		parsed = csvutils.parse(request.FILES['file'], format, ',')
		classutils.update_courses(parsed)
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
	body = ""
	if request.body:
		body = json.loads(request.body)
	try:
		if request.method == "PUT":
			current = classutils.get_course(course)
			if body.has_key("name"):
				if body["name"]:
					try:
						current.enrolment = body["name"] 
						info.setdefault("name", "Updated")
					except Exception as e:
						info.setdefault("name", "Error: " + str(e))
				else:
					info.setdefault("name", "Error: name entry was blank")
			if body.has_key("enrolment"):
				try:
					current.enrolment = body["enrolment"]
					info.setdefault("enrolment", "Updated")
				except Exception as e:
					info.setdefault("enrolment", "Error: " + str(e))
			if body.has_key("department"):
				try:
					current.department = department.objects.get(name = body["department"])
					info.setdefault("department", "Updated")
				except Exception as e:
					info.setdefault("department", "Error: " + str(e))
			if info:
				current.save()
				status = 200
			else:
				info = {"Error" : "Nothing updated"}
				status = 400
		elif request.method == "GET":
			current = classutils.get_course(course)
			if current:
				info = {"name" : current.name, "enrolment" : current.enrolment, "department" : current.department.name}
				status = 200
			else:
				info = {"Error" : "Unknown course code"}
				status = 400
		elif request.method == "DELETE":
			current = classutils.get_course(course)
			if current:
				current.delete()
				info = {course : "successfully deleted"}
				status = 200
			else:
				info = {"Error" : "Unknown course code"}
				status = 400
		elif request.method == "POST":
			body.setdefault("code", course)
			result = classutils.add_course(body)
			if not result:
				info = {course : "successfully added"}
				status = 200
			else:
				info = {"Error" : "Internal error occurred" + result}
				status = 500
		else:
			info = {"Error" : "Unknown request"}
			status = 400
	except Exception as e:
		info = {"Error" : "Internal error occurred " + str(e)}
		status = 500
	data = json.dumps(info)
	return HttpResponse(content = data, status = status)

def instructor_schedule(request, instructor):
    i = Instructor.objects.get(name=instructor)
    context = {"courses": i.myCourses, 'instructor': i.name}
    return render_to_respose('instructor_schedule.html', context, context_instance-RequestContext(request))
