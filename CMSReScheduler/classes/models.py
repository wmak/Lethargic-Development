from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
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
	def create_course(self, name, code, department):
		course = self.create(name=name, code=code, department=department)
		return course

class Course(models.Model):

		code = models.CharField(max_length=9) #ex. CSCC01H3F
		name = models.CharField(max_length=50)
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


class UserProfile(models.Model):
	user = models.OneToOneField('auth.User', related_name='profile', primary_key=True)
	department = models.ForeignKey(Department)
	address = models.CharField(max_length=50)
	room = models.ForeignKey(Room)
	myCourses = models.ManyToManyField(Course)
	role = models.CharField(max_length = 10) # Instructor, admin or chair
	active = models.BooleanField(default=False)


	def __str__(self):  
		return "%s's profile" % self.user  

	def create_user_profile(sender, instance, created, **kwargs):  
		if created:  
		profile, created = UserProfile.objects.get_or_create(user=instance)

	def getSchedule():
		schedule = []
		for c in myCourses:
				schedule.append(CourseSchedule.objects.filter(course = c))
		return schedule

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

	def listClassrooms():
				return Room.objects.get(~Q(capacity = 1))

	def getChairs():
			return Chair.objects.all

	def getInstructorsOfDepartment(dept):
			return Instructor.objects.filter(department = dept)

	def checkEnrolment(courseCode):
			c = Course.objects.get(code = courseCode)
			return c.enrolment

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)

class CourseScheduleManager(models.Manager):
	def create_course_schedule(self, course, room, dayOfWeek, department, length, typeOfSession, enrolment):
		course_schedule = self.create(course=course, room=room, dayOfWeek=dayOfWeek, startTime=startTime, \
			length=length, typeOfSession=typeOfSession, enrolment = enrolment)
		return course_schedule


class CourseSchedule(models.Model):
	course = models.CharField(max_length = 9) #must be the a valid course code
	room = models.CharField(max_length=10) #must be a valid room code
	dayOfWeek = models.CharField(max_length = 9)
	startTime = models.TimeField()
	endTime = models.TimeField() #in minutes
	typeOfSession = models.CharField(max_length = 7) # LEC, TUT or PRA
	enrolment = models.IntegerField()

	@property
	def time_range(self):
		return u"%s - %s" % (self.startTime.strftime("%H:%M"), self.endTime.strftime("%H:%M"))

	def getLength():
		edelta = datetime.timedelta(minutes = endTime.minute, hours = endTime.hour)
		sdelta = datetime.timedelta(minutes = startTime.minute, hours = startTime.hour)
		delta = edelta - sdelta
		return delta.hours * 60 + delta.minutes