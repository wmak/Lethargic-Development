  #!/usr/bin/env python
# encoding: utf-8

import utils.csvutils as csvutils
import utils.classesutils as classutils
import utils.filterutils as filterutils

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, QueryDict
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from forms import UploadCsv, RegisterForm, ProfileEditForm, UserEditForm, AdminUserEditForm, ChangePasswordForm

try:
	import json
except ImportError:
	# Python 2.5
	import simplejson as json


from classes.models import *


'''Constant declaration'''
GOOD_REQUEST = 200
BAD_REQUEST = 400
INTERNAL_ERROR = 500


# Log in the user or raise an error if information given is wrong
def login_view(request):
	# Checks if the user requesting this feature is already logged in. 	
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
				return HttpResponseRedirect("/?login=success")
			else:
				# Show an error page
				return render_to_response("login.html", {"username": username, "message": "The user %s is pending validation." % username, "message_type": "error", "user": request.user}, context_instance=RequestContext(request))
		else:
			# Username and password given don't match or user doesn't exist.
			return render_to_response("login.html", {"username": username, "message": "Incorrect username or password.", "message_type": "error", "user": request.user}, context_instance=RequestContext(request))
	else:
		if request.user.is_authenticated():
			return HttpResponseRedirect("/?login=error")
		else:
			msg, msg_type = "", ""
			if request.GET:
				if "logout" in request.GET:
					msg_type = request.GET['logout']
					if msg_type == "error":
						msg = "An error occurred when logging out. Please try again."
					elif msg_type == "success":
						msg = "You have logged out successfully."
				elif "registration" in request.GET:
					msg_type = request.GET['registration']
					if msg_type == "success":
						msg = "You have successfully been registered. Please log in."
			return render_to_response('login.html', {"message": msg, "message_type": msg_type, "user": request.user}, context_instance=RequestContext(request))

def logout_view(request):
	if request.user.is_authenticated():
		logout(request)
		return HttpResponseRedirect("/login?logout=success")
	else:
		return HttpResponseRedirect("/login?logout=error")

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect("/login?registration=success")
		else:
			return render_to_response("register.html", {"form": form}, context_instance=RequestContext(request))
	else:
		if request.user.is_authenticated():
			return HttpResponseRedirect("/?registration=error")
		else:
			form = RegisterForm()
			return render_to_response("register.html", {"form": form}, context_instance=RequestContext(request))

# This method provides a way for the admin to edit another user's profile
def delete_user(request, username):
	if request.user.is_authenticated():
		# Gets profile of the current user logged in the system
		adminprofile = UserProfile.objects.get(pk=request.user.id)
		# Checks if the user trying to delete is an admin
		if adminprofile.role == 'admin':
			# Finds an user by his username and delete.
			user = User.objects.get(username=username)
			if user == None:
				return HttpResponse("User doesn't exist.")
			else:
				user.delete()
				return HttpResponse("User deleted successfully.")
		else:
			return HttpResponse('You do not have permission to access the page requested.')

# This method provides a way for the user to edit his own profile
def edit_profile(request):
	if request.user.is_authenticated():
		# Gets profile of the current user logged in the system
		profile = UserProfile.objects.get(pk=request.user.id)
		if request.method == 'POST':
			form = ProfileEditForm(request.POST, instance=profile)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/')
		else:
			form = ProfileEditForm(instance=profile)
		return render_to_response("profile.html", {"form": form, "user": request.user,  "notifications": UserProfile.objects.get(user=request.user).notifications, "read_notifications": UserProfile.objects.get(user=request.user).read_notifications }, context_instance=RequestContext(request))

# This method provides a way for the admin to edit another user's profile
def admin_edit_profile(request, username):
	msg, msg_type = "", ""
	if request.user.is_authenticated():
		# Gets profile of the current user logged in the system
		adminprofile = UserProfile.objects.get(pk=request.user.id)
		# Checks if the user trying to edit a profile is an admin
		if adminprofile.role == 'admin':
			user = User.objects.get(username=username)
			userprofile = UserProfile.objects.get(pk=user.id)
			if request.method == 'POST':
				form = ProfileEditForm(request.POST, instance=userprofile)
				if form.is_valid():
					form.save()
					return HttpResponseRedirect('/admin/users/' + username + '/profile/?edit=success')
			else:
				form = ProfileEditForm(instance=userprofile)
			if request.GET and "edit" in request.GET:
				msg_type = request.GET["edit"]
				if msg_type == "success":
					msg = "User profile edited successfully"
				elif msg_type == "error":
					msg = "An error occurred when editing the user profile."
			return render_to_response("admin_edit_profile.html", {"form": form, "message": msg, "message_type": msg_type,  "notifications": UserProfile.objects.get(user=request.user).notifications, "read_notifications": UserProfile.objects.get(user=request.user).read_notifications }, context_instance=RequestContext(request))
		else:
			return HttpResponse('You do not have permission to access the page requested.')

# This method provides a way for the admin to edit another user's information
def admin_edit_user(request, username):
	msg, msg_type = "", ""
	if request.user.is_authenticated():
		# Gets profile of the current user logged in the system
		adminprofile = UserProfile.objects.get(pk=request.user.id)
		# Checks if the user trying to edit another user's information is an admin
		if adminprofile.role == 'admin':
			user = User.objects.get(username=username)
			if request.method == 'POST':
				form = AdminUserEditForm(request.POST, instance=user)
				if form.is_valid():
					form.save()
					return HttpResponseRedirect('/admin/users/' + username + '/edit/?edit=success')
			else:
				form = AdminUserEditForm(instance=user)
			if request.GET and "edit" in request.GET:
				msg_type = request.GET["edit"]
				if msg_type == "success":
					msg = "User edited successfully"
				elif msg_type == "error":
					msg = "An error occurred when editing the user."
			return render_to_response("admin_edit_user.html", {"form": form, "message": msg, "message_type": msg_type,  "notifications": UserProfile.objects.get(user=request.user).notifications, "read_notifications": UserProfile.objects.get(user=request.user).read_notifications }, context_instance=RequestContext(request))
		else:
			return HttpResponse('You do not have permission to access the page requested.')

# This method provides a way for the user to edit his own information
def edit_user(request):
	if request.user.is_authenticated():
		# Gets user info of the current user logged in the system
		if request.method == 'POST':
			form = UserEditForm(request.POST, instance=request.user)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/')
		else:
			form = UserEditForm(instance=request.user)
		c = {'form': form}
		return render_to_response("edit_user.html", c, context_instance=RequestContext(request))

# This method provides a way for the user to change his password
def change_password(request):
	if request.user.is_authenticated():
		# Gets user info of the current user logged in the system
		if request.method == 'POST':
			form = ChangePasswordForm(request.POST)
			if form.is_valid():
				old_password = request.POST['old_password'].strip()
				print old_password
				newpassword = request.POST['newpassword'].strip()
				newpassword2 = request.POST['newpassword2'].strip()

				if old_password and newpassword and newpassword2 == newpassword:
					saveuser = User.objects.get(id=request.user.id)
					if request.user.check_password(old_password):
						saveuser.set_password(request.POST['newpassword']);
						saveuser.save()
						return HttpResponse('Your password was changed.')
					else:
						return HttpResponse('Your old password is incorrect. Please, try again.')
				else:
					return HttpResponse('Insert your old password and new password correctly.')
		else:
			form = ChangePasswordForm()
		c = {'form': form}
		return render_to_response("password_change.html", c, context_instance=RequestContext(request))

def list_users(request):
	if request.user.is_authenticated():
		p = UserProfile.objects.get(pk=request.user.id)
		username = request.user.get_username()
		# Verifies if the user's profile is active or the role is 'admin'
		if p.active and p.role == 'admin':
			users = User.objects.all()
			return render_to_response("admin/users_list.html", {"username": username, "users": users, "user": request.user,  "notifications": UserProfile.objects.get(user=request.user).notifications, "read_notifications": UserProfile.objects.get(user=request.user).read_notifications}, context_instance=RequestContext(request))
		else:
			message = 'Your user is not active or you are not an administrator.'
			return render_to_response("admin/users_list.html", {"username": username, "message": message, "user": request.user,  "notifications": UserProfile.objects.get(user=request.user).notifications, "read_notifications": UserProfile.objects.get(user=request.user).read_notifications}, context_instance=RequestContext(request))
	else:
		message = 'This page is only accessible after logging in. Please log in.'
		return render_to_response("admin/users_list.html", {"message": message, "user": request.user}, context_instance=RequestContext(request))		

#@login_required
def index(request):
	if request.user.is_authenticated():
		msg, msg_type = "", ""
		if request.GET:
			if "login" in request.GET:
				msg_type = request.GET["login"]
				if msg_type == "success":
					msg = "You have successfully been logged in."
				elif msg_type == "error":
					msg = "You are already logged in."
			elif "registration" in request.GET:
				msg = "You are already logged in. You don't need to register."
				msg_type = "error"
		instructor = UserProfile.objects.get(user__username=request.user.username)
		return render(request, 'index.html', {"instructor": instructor, "message": msg, "message_type": msg_type, "user": request.user, "notifications": UserProfile.objects.get(user=request.user).notifications, "read_notifications": UserProfile.objects.get(user=request.user).read_notifications })
	else:
		return HttpResponseRedirect('/login')

#@login_required
def admin(request):
	context = {}
	context["user"] = request.user
	context["notifications"] = UserProfile.objects.get(user=request.user).notifications
	context["read_notifications"] = UserProfile.objects.get(user=request.user).read_notifications
	context["departments"] = Department.objects.all
	return render(request, 'admin/index.html', context)

def admin_upload(request):
	msg, msg_type = "", ""
	if request.method == 'POST':
		try:
			model_type = request.POST["type"]
			form = UploadCsv(model_type, request.FILES)
			if model_type == 'schedule':
				format = ['course', 'typeOfSession', 'dayOfWeek', 'startTime', 'endTime', 'room']
				parser_list = csvutils.parse(request.FILES['file'], format, ',')
				classutils.update_schedule(parser_list, request.POST['instructor'])
			elif model_type == 'room':
			 	capacity, parser_list = csvutils.parse_room_file(request.FILES['file'])
			 	classutils.update_room(parser_list, capacity)
			elif model_type == 'course':
				format = ['code', 'name', 'department']
				parser_list = csvutils.parse(request.FILES['file'], format, ',')
				classutils.update_courses(parser_list)
			elif model_type == 'enrolment':
				format = ['utorid', 'student-number', 'last-name', 'first-names', 'email']
				parser_list = csvutils.parse(request.FILES['file'], format, ',')
				classutils.update_enrolment(parser_list, request.FILES['file'])
			elif model_type == "department_programs":
				format = ['code', 'name']
				parser_list = csvutils.parse(request.FILES['file'], format, ',')
				classutils.update_department_programs(parser_list)
			elif model_type == "students_programs":
				format = ['utorid', 'program-code']
				parser_list = csvutils.parse(request.FILES['file'], format, ',')
				classutils.update_students_programs(parser_list)
			elif model_type == "program_requirements":
				format = ['course_code', 'req_type']
				parser_list = csvutils.parse(request.FILES['file'], format, ',')
				classutils.update_program_requirements(parser_list, request.FILES['file'])
			else:
				msg = "Invalid type."
				msg_type = "error"
		except Exception as e:
			msg = "Invalid file. " + str(e)
			msg_type = "error"

		if msg == "":
			msg = "The %s file has been uploaded." % model_type
			msg_type = "success"
	return render_to_response('admin/upload.html', {'form': UploadCsv(), "departments": Department.objects.all, "message": msg, "message_type": msg_type, "user": request.user, "notifications": UserProfile.objects.get(user=request.user).notifications, "read_notifications": UserProfile.objects.get(user=request.user).read_notifications }, context_instance=RequestContext(request))

def admin_schedule(request, instructor_name):
	context = {}
	try:
		instructor = UserProfile.objects.get(user__username=instructor_name)
		if instructor:
			return render_to_response("admin/schedule.html", {"instructor": instructor, "user": request.user, "notifications": UserProfile.objects.get(user=request.user).notifications, "read_notifications": UserProfile.objects.get(user=request.user).read_notifications}, context_instance=RequestContext(request))
		else:
			return render_to_response("admin/schedule.html", {"message": "Invalid instructor", "message_type": "error", "user": request.user, "notifications": UserProfile.objects.get(user=request.user).notifications, "read_notifications": UserProfile.objects.get(user=request.user).read_notifications}, context_instance=RequestContext(request))
  	except Exception as e:
  		return HttpResponseNotFound(e)

'''This view should receive one string:
1 - which model will be used, shoulb be in the plural for consistency
The strings must be separated by '-'s.
The order of the fields does not matter as long as the values are 
in the same order.'''
@csrf_exempt
def filter(request, model):
	info = ""
	status = GOOD_REQUEST
	if request.method == "GET":
		body = request.GET
		try:
			if model == "rooms":
				qSet = filterutils.filter_rooms(body)
			elif model == "courses":
				qSet = filterutils.filter_courses(body)
			elif model == "schedules":
				qSet = filterutils.filter_schedules(body)
			else:
				info = {"Error" : "Unable to filter. No such model named " + model}
				status = BAD_REQUEST
			JSONSerializer = serializers.get_serializer("json")
			s = JSONSerializer()
			s.serialize(qSet)
			data = s.getvalue()
			status = GOOD_REQUEST
			return HttpResponse(content = data, status = status)
		except Exception as e:
			info = {"Error" : "Error while filtering: " + str(e)}
			status = INTERNAL_ERROR
	else:
		info = {"Error" : "Unable to filter."}
		status = INTERNAL_ERROR
	data = json.dumps(info)
	return HttpResponse(content = data, status = status)


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
	info = {}
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
			if body:
				current = classutils.get_course(course)
				# get fields for course:
				fields = ["code", "name"]
				for field in fields:
					try:
						if body.has_key(field):
							value = body.get(field)
							if value:
								exec("current." + field + " = value")
								info.setdefault(field, "Updated")
							else:
								info.setdefault(field, "Error: name entry was blank")
					except Exception as e:
						info["Error"] = "Error updating"
						info.setdefault(field, "Error: " + str(e))
						status = BAD_REQUEST
				if body.has_key("department"):
					value = body.get("department")
					if value:
						department = current.department
						if (Department.objects.filter(name = body["department"]).count == 1):
							department = Department.objects.get(name = body["department"])
						else:
							department = Department(name = body["department"], numberOfLecturers=0)
							department.save()
						current.department = department
						info.setdefault("department", "Updated")
						status = GOOD_REQUEST
					else:
						info.setdefault(field, "Error: Department entry was blank")
				# Special key switch will switch all details but course and typeOfSession between two CourseSchedules
				if section and body.has_key("switch"):
					try:
						print section
						current = CourseSchedule.objects.filter(course = course, typeOfSession = section)[0]
						next = CourseSchedule.objects.filter(course = body["switch"]["code"], typeOfSession = body["switch"]["section"])[0]
						current.course, next.course = next.course, current.course
						current.typeOfSession, next.typeOfSession = next.typeOfSession, current.typeOfSession
						current.save()
						next.save()
						info = {"info" : course + section + " and " + body["switch"]["code"] + body["switch"]["section"] + " switched"}
						status  = GOOD_REQUEST
					except Exception as e:
						status = BAD_REQUEST
						info.setdefault("department", "Error: " + str(e))
			if status == GOOD_REQUEST:
				notification = "%s has been modified" % course
				classutils.new_notification(notification)
				current.save()
			else:
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
			if result:
				info = {course : "successfully added"}
				status = GOOD_REQUEST
			else:
				info = {"Error" : "Internal error occurred " + str(result)}
				status = INTERNAL_ERROR
		else:
			info = {"Error" : "Unknown request"}
			status = BAD_REQUEST
	except Exception as e:
		info = {"Error" : "Internal error occurred " + str(e)}
		status = INTERNAL_ERROR
	data = json.dumps(info)
	return HttpResponse(content = data, status = status)

def add_course(request):
	msg, msg_type = "", ""
	if request.GET and "add" in request.GET:
		msg_type = request.GET["add"]
		if msg_type == "success":
			msg = "The course has successfully been added."
		elif msg_type == "error":
			msg = "An error occurred while adding the course."
	return render_to_response("add_course.html", {"user": request.user, "message": msg, "message_type": msg_type, "notifications": UserProfile.objects.get(user=request.user).notifications, "read_notifications": UserProfile.objects.get(user=request.user).read_notifications}, context_instance=RequestContext(request))

def delete_course(request):
	msg, msg_type = "", ""
	if request.GET and "delete" in request.GET:
		msg_type = request.GET["delete"]
		if msg_type == "success":
			msg = "The course has successfully been deleted."
		elif msg_type == "error":
			msg = "An error occurred while deleting the course."
	courses = UserProfile.objects.get(user__username=request.user.username).myCourses.all()
	return render_to_response("delete_course.html", {"courses": courses, "user": request.user, "message": msg, "message_type": msg_type, "notifications": UserProfile.objects.get(user=request.user).notifications, "read_notifications": UserProfile.objects.get(user=request.user).read_notifications}, context_instance=RequestContext(request))

def switch_course(request):
	msg, msg_type = "", ""
	if request.GET and "switch" in request.GET:
		msg_type = request.GET["switch"]
		if msg_type == "success":
			msg = "The courses have successfully been switched."
		elif msg_type == "error":
			msg = "An error occurred while switching the courses."
	courses = UserProfile.objects.get(user__username=request.user.username).myCourses.all()
	return render_to_response("switch_course.html", {"courses": courses, "user": request.user, "message": msg, "message_type": msg_type, "notifications": UserProfile.objects.get(user=request.user).notifications, "read_notifications": UserProfile.objects.get(user=request.user).read_notifications}, context_instance=RequestContext(request))


def room_capacities(request):
	''' Takes in a request and returns all of the rooms, ordered by their code, and their capacities to a webpage 
	'''

	try:
		room_objects = Room.objects.order_by('code')

		if room_objects:
			rooms = []
			capacities = []

			for item in room_objects:
				rooms.append(item.code)
				capacities.append(item.capacity)
			super_list = zip(rooms, capacities)

			context = {'list': super_list}

			return render_to_response('room_capacities.html', context, context_instance=RequestContext(request))
		else:
			return HttpResponseNotFound('<h1>Page not found. No Rooms. </h1>')

	except Exception as e:
		return HttpResponseNotFound(e)


def room_schedule(request, room_code):
	''' takes in a request object and the room from the url and makes a query to the database to find all the courses
		that use that room and returns them to a webpage  
	'''
	try:
		c = CourseSchedule.objects.filter(room=room_code)

		if c:
			course_code = []
			course_name = []
			start_times = []
			end_times = []
			class_type = []
			days = []
			


			for course in c:
				new_course = Course.objects.get(code=course.course)
				course_code.append(new_course.code)
				course_name.append(new_course.name)
				start_times.append(course.startTime)
				end_times.append(course.endTime)
				class_type.append(course.typeOfSession)
				days.append(course.dayOfWeek)

			super_list = zip(course_code, class_type, course_name, days, start_times, end_times)

			context = {'room': room_code, 'list': super_list}
			return render_to_response('room_schedule.html', context, context_instance=RequestContext(request))
		else:
			return HttpResponseNotFound('<h1>Page not found. Invalid Room </h1>')
	except Exception as e:
		return HttpResponseNotFound(e)


def department_schedule(request, department_name, instructor_name):
	''' Takes in a request object as well as two strings for the name of the department and the name
		of the instructor. Returns this a schedule of the instructor to departments.html.
	'''

	try:
		department = Department.objects.get(name=department_name)
		instructor = Instructor.objects.get(name=instructor_name)

		if department and  instructor:
			chair = Chair.objects.get(deartment=department_name)
			courses = instructor.getSchedule()
			course_code = []
			course_name = []
			class_type = []
			days = []
			room = []
			

			for c in courses:
				course = Course.objects.get(code=c.course)
				course_code.append(course.code)
				course_name.append(course.name)
				start_times.append(c.startTime)
				end_times.append(c.endTime)
				class_type.append(c.typeOfSession)
				days.append(c.dayOfWeek)
				room.append(c.room)

			super_list = zip(course_code, class_type, course_name, days, start_times, end_times)


			context = {'room': room, }

			return render_to_response('departments.html', context, context_instance=RequestContext(request))
		else:
			return HttpResponseNotFound('<h1>Page not found. Invalid department or instructor name </h1>')
			
	except Exception as e:
		return HttpResponseNotFound(e)

@csrf_exempt
def instructors(request, department_name):
	info = {"Error" : "Nothing happened somehow"}
	status = INTERNAL_ERROR
	try:
		department = Department.objects.get(name=department_name)

		if department:
			instructors = []
			for instructor in UserProfile.objects.filter(department__name=department.name):
				instructors += [instructor.user.username]
			info = {"instructors" : instructors }
			status = GOOD_REQUEST
		else:
			info = {"Error" : "Department could not be found"}
			status = BAD_REQUEST
	except Exception as e:
		info = {"Error" : str(e)}
	data = json.dumps(info)
	return HttpResponse(content = data, status = status)

@csrf_exempt
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
			info = classutils.get_notifications(user_id)
			status = GOOD_REQUEST
		elif request.method == "PUT":
			data = classutils.get_notifications(user_id)
			status = BAD_REQUEST
			if body.has_key("read"):
				if type(body["read"]) == list:
					if classutils.update_notifications(user_id, body["read"]):
						status = GOOD_REQUEST
						info = {"Status" : "Updated successfully"}
					else:
						status = INTERNAL_ERROR
	except Exception as e:
		info = {"Error" : str(e)}
	data = json.dumps(info)
	return HttpResponse(content = data, status = status)

@csrf_exempt
def export(request, model):
	from django.core.management import call_command
	try:
		output = open("datadump.json",'w')
		if model == "all":
			call_command("dumpdata", format='json',indent=4, stdout=output)
		else:
			call_command("dumpdata", model, format='json',indent=4, stdout=output)
		output.close()
		output = open("datadump.json",'r+')
		body = output.read()
		status = GOOD_REQUEST
	except Exception as e:
		status = BAD_REQUEST
		body = "An Error occurred: " + str(e)
	return HttpResponse(content = body, status = status)
