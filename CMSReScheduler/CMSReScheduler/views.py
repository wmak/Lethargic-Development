#!/usr/bin/env python
# encoding: utf-8

import utils.csvutils as csvutils
import utils.classesutils as classutils

from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from forms import UploadCsv, RegisterForm

try:
	import json
except ImportError:
	# Python 2.5
	import simplejson as json

from classes.models import Course, Department, CourseSchedule, UserProfile, Notifications

'''Constant declaration'''
GOOD_REQUEST = 200
BAD_REQUEST = 400
INTERNAL_ERROR = 500

# Log in the user or raise an error if information given is wrong
def login_view(request):
	if request.POST:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = authenticate(username=username, password=password)
		# Gets user profile by user id if username and password given match
		if user is not None:
			p = UserProfile.objects.get(pk=user.id)
			# Verifies if the user's profile is active or the role is 'admin'
			if p.active or p.role == 'admin':
				login(request, user)
				# Redirect to a success page depending on the user's role.
				return HttpResponseRedirect("/")
			else:
				# Show an error page
				return HttpResponse('Your user is inactive or doesn\'t exist.')
		else:
			# Username and password given don't match or user doesn't exist.
			return HttpResponse('Wrong username or password.')
	else:
		return render_to_response('login.html', context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	# Redirect to a success page.
	return HttpResponse("Logged out.")

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect('/')
	else:
		form = RegisterForm()
	c = {'form': form}
	return render_to_response("register.html", c, context_instance=RequestContext(request))

#@login_required
def index(request):
	return render(request, 'index.html')

#@login_required
def admin(request):
	# TODO: Filter the results by instructor
	daysOfWeek = ["MO", "TU", "WE", "TH", "FR"]
	context = {}
	for day in daysOfWeek:
		context[day] = CourseSchedule.objects.filter(dayOfWeek=day).order_by("startTime")
	return render(request, 'admin/index.html', context)

def admin_upload(request):
	msg, msg_type = "", ""
	if request.method == 'POST':
		try:
			model_type = request.POST["type"]
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
				format = ['code', 'name', 'department']
				parser_list = csvutils.parse(request.FILES['file'], format, ',')
				classutils.update_courses(parser_list)
			# elif model_type == 'department':
			# 	format = ['code', 'name']
			# 	parser_list = csvutils.parse(request.FILES['file'], format, ',')
			# 	csvutils.update_departments(parser_list)
			else:
				msg = "Invalid type."
				msg_type = "error"
		except Exception as e:
			msg = "Invalid file."
			msg_type = "error"

		if msg == "":
			msg = "The %s file has been uploaded." % model_type
			msg_type = "success"
	return render_to_response('admin/upload.html', {'form': UploadCsv(), "departments": Department.objects.all, "message": msg, "message_type": msg_type}, context_instance=RequestContext(request))

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
				notification = "%s has been modified" % course
				classutils.new_notification(notification)
				current.save()
				status = GOOD_REQUEST
			else:
				info = {"Error" : "Nothing updated"}
				status = BAD_REQUEST
		elif request.method == "GET":
			current = classutils.get_course(course)
			if current:
				info = {"name" : current.name, "department" : current.department.name}
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

def user(request, user_id):
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
		if request.method == "GET":
			info = {"notifications" : json.dumps(classutils.get_notifications(user_id))}
			status = GOOD_REQUEST
	except Exception as e:
		info.setdefault("department", "Error: " + str(e))
	data = json.dumps(info)
	return HttpResponse(content = data, status = status)


def instructor_schedule(request, instructor):
	i = Instructor.objects.get(name=instructor)
	context = {"courses": i.myCourses, 'instructor': i.name}
	return render_to_response('instructor_schedule.html', context, context_instance-RequestContext(request))
