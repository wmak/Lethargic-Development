#!/usr/bin/env python
# encoding: utf-8

import utils.csvutils as csvutils
import utils.classesutils as classutils

from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from forms import UploadCsv
from forms import InstructorRegistrationForm
import simplejson as json

from classes.models import Course, Department, CourseSchedule

def csvimport(request, model_type):
	''' NOTE: for now I have a single url for this. I can send them  each to a certain page if you guys prefer.
	This is still very much up for debate. Let me know what you all think '''
	model_type = model_type.strip().lower()
	if request.method != 'POST':
		return render_to_response('csvimport.html', {'form': UploadCsv()}, context_instance=RequestContext(request))

	form = UploadCsv(model_type, request.FILES)
	if model_type == 'schedule':
		format = ['course', 'room', 'dayOfWeek', 'startTime', 'endTime', 'typeOfSession']
		parser_list = csvutils.parse(request.FILES['file'], format, ',')
		classutils.update_schedule(parser_list)
	# elif model_type == 'room':
	# 	format = ['code', 'name', 'building']
	# 	parser_list = csvutils.parse(request.FILES['file'], format, ',')
	# 	csvutils.update_rooms(parser_list)
	elif model_type == 'course':
		format = ['code', 'name', 'enrolment', 'department']
		parser_list = csvutils.parse(request.FILES['file'], format, ',')
		classutils.update_courses(parser_list)
	# elif model_type == 'department':
	# 	format = ['code', 'name']
	# 	parser_list = csvutils.parse(request.FILES['file'], format, ',')
	# 	csvutils.update_departments(parser_list)
	else:
		return HttpResponse('Invalid model_type!')
	return HttpResponse('The %s file has been uploaded!' % model_type)

def admin(request):
	return render(request, 'admin/index.html')

def admin_upload(request):
	return render(request, 'admin/upload.html')

def registration(request, type):
    if request.method == 'POST':
        if type == 'instructor':
            form = InstructorRegistrationForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                return HttpResponse('User registered successfully.')
            else:
                return HttpResponse('Invalid form.')
        else:
            return HttpResponse('Select one of the roles available.')
    else:
        form = InstructorRegistrationForm()
    return render_to_response('registration.html', {'form': form}, context_instance=RequestContext(request))

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
				times = []
				for time in CourseSchedule.objects.filter(course = current):
					times.append(time.time_range)
				info.setdefault("Times", times)
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
