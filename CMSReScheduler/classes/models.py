from django.db import models
from datetime import datetime
# Create your models here.

class Department(models.Model):
	name = models.CharField(max_length=30)
	numberOfLecturers = models.IntegerField()

	def __unicode__(self):
		return self.name


class Course(models.Model):

	code = models.CharField(max_length=9) #ex. CSCC01H3F
	name = models.CharField(max_length=50)
	enrolment = models.IntegerField()
	department = models.ForeignKey(Department)

	def __unicode__(self):
		return u'%s - %s' % (self.code, self.name)

class Room(models.Model):
	code = models.CharField(max_length=10) #ex. IC220
	capacity = models.IntegerField()

	def __unicode__(self):
		return self.code

	def getSchedule():
		return CourseSchedule.objects.filter(room = self)


class User(models.Model):
	name = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
	email = models.EmailField()
	department = models.ForeignKey(Department)

	def __unicode__(self):
		return self.name

class Instructor(User):			#incomplete
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
	def viewDepartmentInstructors():
		return Instructor.objects.filter(department = self.department)

	def viewInstructorsSchedules():
		instructors = viewDepartmentInstructors();
		schedules = []
		for i in instructors:
			schedules.append(i.getSchedule())
		return schedules



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


class CourseSchedule(models.Model):
	course = models.ForeignKey(Course)
	room = models.ForeignKey(Room)
	dayOfWeek = models.CharField(max_length = 9)
	startTime = models.TimeField()
	length = models.IntegerField() #in minutes
	typeOfSession = models.CharField(max_length = 3) # LEC, TUT or PRA
	section = models.CharField(max_length = 4) #0001

	@property
	def time_range(self):		
		return u"%s - %s" % (self.startTime.strftime("%H:%M"), self.calcEndTime().strftime("%H:%M"))

	def calcEndTime():
		h = length / 60
		m = length % 60
		endHour = startTime.hour + h
		endMinutes = startTime.minute + m
		if endMinutes >= 60:
			endHour += 1
			endMinutes -= 60
		endTime = datetime.time(endHour, endMinutes)
		return endTime

