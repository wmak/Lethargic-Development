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


#This view should receive three strings:
#1 - which model will be used, shoulb be in the plural for consistency
#2 - fields on which we should filter
#3 - values for each of the fields passed in 1.
#The strings must be separated by '-'s.
#The order of the fields does not matter as long as the values are 
#in the same order.
def filter(request, model, fields, values): 
    if request.method == "GET":
        status = 200
        try:
            fList = fields.split('-')
            vList = values.split('-')
            qSet = []
            if(fList.length != vList.length):
                data = json.dumps("Unable to filter. Number of fields does not match the number of values.")
                status = 400
                return HttpResponse(content = data, status = status)
            if model == "rooms":
                qSet = filterRooms(fList, vList)
            elif model == "courses":
                qSet = filterCourses(fList, vList)
            else:
                data = json.dumps("Unable to filter. No such model named %s" % (model))
                status = 400
                return HttpResponse(content = data, status = status)
            JSONSerializer = serializers.get_serializer("json")
            s = JSONSerializer()
            s.serialize(qSet)
            data = s.getvalue()
            status = 200
            return HttpResponse(content = data, status = status)
        except Exception as e:
            data = json.dumps("Error while filtering")
            status = 500
            return HttpResponse(content = data, status = status)
    else:
        data = json.dumps("Unable to filter.")
        status = 500
        return HttpResponse(content = data, status = status)

# when you change the registration url, dont forget to edit 'type' here as well

# The registration will consider the user role 
# because there are 3 differente classes to deal with users
def registration(request, user_role):
	if request.method == 'POST':
		# Depending on the role, the appropriate form will be rendered
		if user_role == 'instructor':
			form = InstructorRegistrationForm(request.POST)
			if form.is_valid():
				new_user = form.save()
				info = 'User registered successfully.'
				status = 200
			else:
				info = 'Invalid form.'
				status = 400
		else:
			# There is no "neutral user", so every registration has to include the role
			info = 'Select one of the roles available.'
			status = 400
		return render_to_response(content=info, status=status)
	else:
		form = InstructorRegistrationForm()
		status = 200
	return render_to_response('registration.html', {'form': form}, status=status, context_instance=RequestContext(request))

@csrf_exempt
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
	status = 500
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
					status  = 200
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
					times.append(time.typeOfSession + ":" + time.time_range)
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
