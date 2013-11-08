#!/usr/bin/env python
# encoding: utf-8

import utils.csvutils as csvutils
import utils.classesutils as classutils

from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from forms import UploadCsv, InstructorRegistrationForm
try:
	import json
except ImportError:
	# Python 2.5
	import simplejson as json

from classes.models import Course, Department, CourseSchedule

'''Constant declaration'''
GOOD_REQUEST = 200
BAD_REQUEST = 400
INTERNAL_ERROR = 500

def csvimport(request, model_type):
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

def index(request):
	return render(request, 'index.html')

def admin(request):
	# TODO: Filter the results by instructor
	daysOfWeek = ["MO", "TU", "WE", "TH", "FR"]
	context = {}
	for day in daysOfWeek:
		context[day] = CourseSchedule.objects.filter(dayOfWeek=day).order_by("startTime")
	return render(request, 'admin/index.html', context)

def admin_upload(request):
	return render(request, 'admin/upload.html', {"departments": Department.objects.all})


'''This view should receive three strings:
1 - which model will be used, shoulb be in the plural for consistency
2 - fields on which we should filter
3 - values for each of the fields passed in 1.
The strings must be separated by '-'s.
The order of the fields does not matter as long as the values are 
in the same order.'''
def filter(request, model, fields, values): 
	if request.method == "GET":
		status = GOOD_REQUEST
		try:
			fList = fields.split('-')
			vList = values.split('-')
			qSet = []
			if(fList.length != vList.length):
				data = json.dumps("Unable to filter. Number of fields does not match the number of values.")
				status = BAD_REQUEST
				return HttpResponse(content = data, status = status)
			if model == "rooms":
				qSet = filterRooms(fList, vList)
			elif model == "courses":
				qSet = filterCourses(fList, vList)
			else:
				data = json.dumps("Unable to filter. No such model named %s" % (model))
				status = BAD_REQUEST
				return HttpResponse(content = data, status = status)
			JSONSerializer = serializers.get_serializer("json")
			s = JSONSerializer()
			s.serialize(qSet)
			data = s.getvalue()
			status = GOOD_REQUEST
			return HttpResponse(content = data, status = status)
		except Exception as e:
			data = json.dumps("Error while filtering")
			status = INTERNAL_ERROR
			return HttpResponse(content = data, status = status)
	else:
		data = json.dumps("Unable to filter.")
		status = INTERNAL_ERROR
		return HttpResponse(content = data, status = status)

'''The registration will consider the user role 
because there are 3 differente classes to deal with users'''
def registration(request, user_role):
	if request.method == 'POST':
		# Depending on the role, the appropriate form will be rendered
		if user_role == 'instructor':
			form = InstructorRegistrationForm(request.POST)
			if form.is_valid():
				new_user = form.save()
				info = 'User registered successfully.'
				status = GOOD_REQUEST
			else:
				info = 'Invalid form.'
				status = BAD_REQUEST
		else:
			# There is no "neutral user", so every registration has to include the role
			info = 'Select one of the roles available.'
			status = BAD_REQUEST
		return render_to_response(content=info, status=status)
	else:
		form = InstructorRegistrationForm()
		status = GOOD_REQUEST
	return render_to_response('registration.html', {'form': form}, status=status, context_instance=RequestContext(request))

def course(request, course, section):
	''' 
		Perform an action on a course 
		PUT -- Modify the course
			request body = {
				"name" : "new name",	# Changes the courses name to new name
				"enrolment" : val,		# Changes the courses enrolment to val, either a string or int.
				"department" : "new",	# Changes the courses department to new
				"switch" : {"code" : "Course code to switch with", "section" : "the section to swap with"},
			}
		GET -- All relevant information pertaining to this course
			No request body required
		DELETE -- Remove this course from the schedule (It will still exist as a course)
			No request body required
		POST -- Add a new course
			request body = {
				"code" : "new value",
				"name" : "new value",
				"enrolment" : "new value",
				"department" : "new value",
			}
	'''
	info = {"Error" : "Nothing happened somehow"}
	status = INTERNAL_ERROR
	body = ""
	# If the request has a body, assume that it is json. And parse it.
	if request.body:
		try:
			body = json.loads(request.body)
		except:
			info = {"Error" : "Badly formatted Json"}
			body = None
	try:
		# Modifying a course if its a put request
		if request.method == "PUT":
			current = classutils.get_course(course)
			# if the body has a name key, then it's a request for changing the name
			if body.has_key("name"):
				if body["name"]:
					try:
						current.enrolment = body["name"] 
						info.setdefault("name", "Updated")
					except Exception as e:
						info.setdefault("name", "Error: " + str(e))
				else:
					info.setdefault("name", "Error: name entry was blank")
			# same Applies to enrolment
			if body.has_key("enrolment"):
				try:
					current.enrolment = body["enrolment"]
					info.setdefault("enrolment", "Updated")
				except Exception as e:
					info.setdefault("enrolment", "Error: " + str(e))
			# and as well with department, these are separate if statements if the user wants to make multiple changes in one request
			if body.has_key("department"):
				try:
					current.department = department.objects.get(name = body["department"])
					info.setdefault("department", "Updated")
				except Exception as e:
					info.setdefault("department", "Error: " + str(e))
			# Special key switch will switch all details but course and typeOfSession between two CourseSchedules
			if section and body.has_key("switch"):
				try:
					current = CourseSchedule.objects.filter(course = current, typeOfSession = section)[0]
					to_switch = classutils.get_course(body["switch"]["code"])
					next = CourseSchedule.objects.filter(course = to_switch, typeOfSession = body["switch"]["section"])[0]
					current.course, next.course = next.course, current.course
					current.typeOfSession, next.typeOfSession = next.typeOfSession, current.typeOfSession
					current.save()
					next.save()
					info = {"info" : course + section + " and " + body["switch"]["code"] + body["switch"]["section"] + " switched"}
					status  = GOOD_REQUEST
				except Exception as e:
					info.setdefault("department", "Error: " + str(e))
			if info:
				current.save()
				status = GOOD_REQUEST
			else:
				info = {"Error" : "Nothing updated"}
				status = BAD_REQUEST
		elif request.method == "GET":
			current = classutils.get_course(course)
			if current:
				info = {"name" : current.name, "enrolment" : current.enrolment, "department" : current.department.name}
				times = []
				for time in CourseSchedule.objects.filter(course = current):
					times.append(time.typeOfSession + ":" + time.time_range)
				info.setdefault("Times", times)
				status = GOOD_REQUEST
			else:
				info = {"Error" : "Unknown course code"}
				status = BAD_REQUEST
		elif request.method == "DELETE":
			current = classutils.get_course(course)
			if current:
				current.delete()
				info = {course : "successfully deleted"}
				status = GOOD_REQUEST
			else:
				info = {"Error" : "Unknown course code"}
				status = BAD_REQUEST
		elif request.method == "POST":
			body.setdefault("code", course)
			result = classutils.add_course(body)
			if not result:
				info = {course : "successfully added"}
				status = GOOD_REQUEST
			else:
				info = {"Error" : "Internal error occurred" + result}
				status = INTERNAL_ERROR
		else:
			info = {"Error" : "Unknown request"}
			status = BAD_REQUEST
	except Exception as e:
		info = {"Error" : "Internal error occurred " + str(e)}
		status = INTERNAL_ERROR
	data = json.dumps(info)
	return HttpResponse(content = data, status = status)

def instructor_schedule(request, instructor):
	i = Instructor.objects.get(name=instructor)
	context = {"courses": i.myCourses, 'instructor': i.name}
	return render_to_respose('instructor_schedule.html', context, context_instance-RequestContext(request))

def room_schedule(request, room_code):
	''' takes in a request object and the room from the url and makes a query to the database to find all the courses
		that use that room and returns them to a webpage  
	'''
	room = Room.objects.get(code=room_code)
	room_schedule = room.getSchedule()
	context = {'room': room.code, 'schedule': room_schedule}
	return render_to_respose(room_schedule.html, context, context_instance-RequestContext(request))



