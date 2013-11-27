#!/usr/bin/env python
# encoding: utf-8

from classes.models import Course, Department, CourseSchedule, Room, UserProfile, Notifications, Student, Program, RequiredCourse
from datetime import datetime

def update_courses(items):
	for item in items:
		entry = Course.objects.filter(code=item["code"])
		if entry.count() == 0:
			add_course(item, True)

def update_schedule(items):
	for item in items:
		cs = CourseSchedule.objects.filter(course = item["course"], typeOfSession = item["typeOfSession"], dayOfWeek = item["dayOfWeek"])
		if cs.count() == 0:
			status = add_schedule(item, True)
			if not status:
				return status
	return "Successfully Updated"

def update_enrolment(items, file):
	name, ext = str(file).split('.')
	cs = CourseSchedule.objects.filter(course = name)
	if cs.count() == 0:
		return "This course is not present in any Schedule. Unable to update the enrolment."
	else:
		course = Course.objects.filter(code = name)
		cs.update(enrolment = len(items))
		for s in items:
			student = Student.objects.filter(utorid = s["utorid"]);
			if student.count() == 0:
				student = Student(utorid = s["utorid"], studentNumber = s["student-number"], lastName = s["last-name"], firstName = s["first-names"], email = s["email"])
				student.save()
				student.courses.add(course[0])
				student.save()
			else:
				for st in student:
					st.courses.add(course[0])
					st.save()
		return "Successfully Updated"

def update_room(room_schedule, capacity):
	room = Room.objects.filter(code = room_schedule[0].room)
	if room.count() == 0:
		r = Room(code = room_schedule[0].room, capacity = capacity)
		r.save()
	else:
		room.update(capacity = capacity)
	for s in room_schedule:
		if s.course == "":
			continue
		item = CourseSchedule.objects.filter(course = s.course, typeOfSession = s.typeOfSession, dayOfWeek = s.dayOfWeek)
		if item.count() == 0:
			s.save()
		else:
			item.update(room = s.room, endTime = s.endTime)

def update_department_programs(items):
	for item in items:
		p = Program.objects.filter(code = item["code"])
		if p.count() == 0:
			p = Program(code = item["code"], name = item["name"])
			p.save()
	return "Successfully Updated"

def update_students_programs(items):
	for item in items:
		p = Program.objects.filter(code = item["program-code"])
		if p.count() == 0:
			return "Unable to update students programs. There is no such program: " + item["program-code"]
		s = Student.objects.filter(utorid = item["utorid"])
		if s.count() == 0:
			return "Unable to update students programs. There is no such student: " + item["utorid"]
		else:
			s.update(programCode = p[0])
	return "Successfully Updated"

def update_program_requirements(items, file):
	msg = ""
	pCode = str(file).split('.')[0]
	p = Program.objects.filter(code = pCode)
	if p.count() == 0:
		return "Unable to update program requirements. There is no such program: " + pCode
	for item in items:
		c = Course.objects.filter(code = item["course_code"])
		if c.count() == 0:
			msg += ("There is no such course: " + item["course_code"] + "\n")
		else:
			rc = RequiredCourse.objects.filter(code = c[0], req_type = item["req_type"])
			if rc.count() == 0:
				req = RequiredCourse(code = c[0], req_type = item["req_type"])
				req.save()
				p[0].requiredCourses.add(req)
				p[0].save()
			else:
				p[0].requiredCourses.add(rc[0])
				p[0].save()
	if msg == "":
		return "Successfully Updated"
	else:
		return msg


def get_course(code):
	courses = Course.objects.filter(code=code)
	if courses:
		return courses[0]
	else:
		return None

def add_course(item, create_department = False):
	try:
		if create_department and Department.objects.filter(name = item["department"]).count() == 0:
			department = Department(name = item["department"], numberOfLecturers=0)
			department.save()
		elif (Department.objects.filter(name = item["department"]).count() == 1):
			department = Department.objects.get(name = item["department"])
		else:
			return "Error Department doesn't exist"
		course = Course(code=item["code"], name=item["name"], department=department)
		course.save()
		return course
	except Exception as e:
		print "EXCEPTION " + str(e)
		return e

def add_schedule(item, create_room = True, create_course = True):
	startTime = datetime.strptime(item["startTime"], "%H:%M")
	endTime = datetime.strptime(item["endTime"], "%H:%M")
	try:
		if create_room and Room.objects.filter(code=item["room"]).count() == 0:
			room = Room(code = item["room"], capacity=0)
			room.save()
		elif Room.objects.filter(code=item["room"]).count() == 1:
			room = Room.objects.get(code=item["room"])
		else:
			return "Error: room doesn't exist"
		if create_course and Course.objects.filter(code=item["course"]).count() == 0:
			course = add_course({"code" : item["course"], "name" : "Default Name", "department" : "Default Department"}, create_department = True)
		elif Course.objects.filter(code=item["course"]).count() == 1:
			course = Course.objects.get(code=item["course"])
		else:
			return "Error: course doesn't exist"
		CourseSchedule(course=course.code, room=room, dayOfWeek=item["dayOfWeek"], startTime=startTime, endTime=endTime, typeOfSession=item["typeOfSession"], enrolment = 0).save()
		return True
	except Exception as e:
		print "EXCEPTION " + str(e)
		return e

def new_notification(text):
	#TODO, filter by instructors who own the course
	notification = Notifications(data = text)
	notification.save()
	users = UserProfile.objects.filter(notify = True)
	for user in users:
		user.notifications.add(notification)
		user.save()

def get_notifications(user_id):
	user = UserProfile.objects.get(pk = user_id)
	notifications = user.notifications.all()
	read_notifications = user.read_notifications.all()
	unread = []
	read = []
	for notification in notifications:
		unread.append(str(notification.data))
	for notification in read_notifications:
		read.append(str(notification.data))
	return {"read" : read, "unread" : unread}

def update_notifications(user_id, new_notifications):
	try:
		user = UserProfile.objects.get(pk = user_id)
		notifications = user.notifications.all()
		for notification in notifications:
			if str(notification.data) in new_notifications:
				user.notifications.remove(notification)
				user.read_notifications.add(notification)
		user.save()
	except Exception as e:
		return False
	return True

