from django.db import models
from datetime import datetime
# Create your models here.
class DepartmentManager(models.Manager):
	def create_department(self, name, numberOfLecturers):
		department = self.create(name=name, numberOfLecturers=numberOfLecturers)
		return department

class Department(models.Model):
		name = models.CharField(max_length=30)
		numberOfLecturers = models.IntegerField()

		def __unicode__(self):
				return self.name

class CourseManager(models.Manager):
	def create_course(self, name, code, enrolment, department):
		course = self.create(name=name, code=code, enrolment=enrolment, department=department)
		return course

class Course(models.Model):

		code = models.CharField(max_length=9) #ex. CSCC01H3F
		name = models.CharField(max_length=50)
		enrolment = models.IntegerField()
		department = models.ForeignKey(Department)

		def __unicode__(self):
				return u'%s - %s' % (self.code, self.name)

class RoomManager(models.Manager):

	def create_room(self, code, capacity):
		room = self.create(code=code, capacity=capacity)
		return rooom

class Room(models.Model):
		code = models.CharField(max_length=10) #ex. IC220
		capacity = models.IntegerField()

		def __unicode__(self):
				return self.code

		def getSchedule():
				return CourseSchedule.objects.filter(room = self)


class UserManager(models.Manager):
	def create_user(self, name, address, email, department):
		user = self.create(name=name, address=address, email=email, department=department)
		return user

	def getSchedule():
		return CourseSchedule.objects.filter(room = self)


class User(models.Model):
		name = models.CharField(max_length=30)
		address = models.CharField(max_length=50)
		email = models.EmailField()
		department = models.ForeignKey(Department)

		def __unicode__(self):
				return self.name


class Instructor(User):                        #incomplete
		room = models.ForeignKey(Room)
		myCourses = models.ManyToManyField(Course)

		def __unicode__(self):
				return u'Professor %s' % (self.name)

		def getSchedule():
				schedule = []
				for c in myCourses:
						schedule.append(CourseSchedule.objects.filter(course = c))
				return schedule

class Chair(Instructor):
		
	#def prohibitChanges():
		#TODO

	def viewDepartmentInstructors():
		return Instructor.objects.filter(department = self.department)
	
	def viewInstructorsSchedules():
		instructors = viewDepartmentInstructors();
		schedules = []
		for i in instructors:
			schedules.append(i.getSchedule())
		return schedules

	def getSchedule():
		schedule = []
		for c in myCourses:
			schedule.append(CourseSchedule.objects.filter(course = c))
		return schedule


class UndergradAdminAssistant(User):

		#This method returns all classrooms, that is,
		#rooms with capacity different from 1.
		def listClassrooms():
				return Room.objects.get(~Q(capacity = 1))

		def getChairs():
				return Chair.objects.all

		def getInstructorsOfDepartment(dept):
				return Instructor.objects.filter(department = dept)

		def checkEnrolment(courseCode):
				c = Course.objects.get(code = courseCode)
				return c.enrolment


class CourseScheduleManager(models.Manager):
	def create_course_schedule(self, course, room, dayOfWeek, department, length, typeOfSession):
		course_schedule = self.create(course=course, room=room, dayOfWeek=dayOfWeek, startTime=startTime, \
			length=length, typeOfSession=typeOfSession)
		return course_schedule


class CourseSchedule(models.Model):
	course = models.ForeignKey(Course)
	room = models.ForeignKey(Room)
	dayOfWeek = models.CharField(max_length = 9)
	startTime = models.TimeField()
	endtime = models.TimeField() #in minutes
	typeOfSession = models.CharField(max_length = 3) # LEC, TUT or PRA
	section = models.CharField(max_length = 4) #0001

	@property
	def time_range(self):
		return u"%s - %s" % (self.startTime.strftime("%H:%M"), self.endTime.strftime("%H:%M"))

	def getLength():
		edelta = datetime.timedelta(minutes = endTime.minute, hours = endTime.hour)
		sdelta = datetime.timedelta(minutes = startTime.minute, hours = startTime.hour)
		delta = edelta - sdelta
		return delta.hours * 60 + delta.minutes