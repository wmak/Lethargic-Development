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



class Notifications(models.Model):
	data = models.CharField(max_length=128)#Change to width of the text box

#Profile connected to each User created. Fields are not required because
#for each user created, a profile is automatically created also.
#The user registration doesn't include department, courses and so on
class UserProfile(models.Model):
	user = models.OneToOneField('auth.User', related_name='profile', primary_key=True)
	department = models.ForeignKey(Department, null=True, blank=True)
	address = models.CharField(max_length=50)
	myCourses = models.ManyToManyField(Course, null=True, blank=True)
	role = models.CharField(max_length = 10) # Instructor, admin or chair
	notifications = models.ManyToManyField(Notifications)
	read_notifications = models.ManyToManyField(Notifications, related_name='notifications')
	#Every user, when created, is inactive.
	notify = models.BooleanField(default=True)
	active = models.BooleanField(default=False)

	def __str__(self):  
		return "%s's profile" % self.user  

	def create_user_profile(sender, instance, created, **kwargs):  
		if created:  
			profile, created = UserProfile.objects.get_or_create(user=instance)

	def is_active():
		return active

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		profile, created = UserProfile.objects.get_or_create(user=instance)
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
	endTime = models.TimeField()
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

	def __unicode__(self):
		return u'%s %s - %s: %s %s %s' % (self.dayOfWeek, self.startTime, self.endTime, self.course, self.typeOfSession, self.room)

class RequiredCourse(models.Model):
	code = models.ForeignKey(Course)
	req_type = models.CharField(max_length = 10) 

class Program(models.Model):
	code = models.CharField(max_length = 10)
	name = models.CharField(max_length = 100)
	requiredCourses = models.ManyToManyField(RequiredCourse)

class Student(models.Model):
	utorid = models.CharField(max_length = 10)
	studentNumber = models.CharField(max_length = 10)
	lastName = models.CharField(max_length = 50)
	firstName = models.CharField(max_length = 20)
	email = models.EmailField()
	programCode = models.ForeignKey(Program, null = True, blank = True)
	courses = models.ManyToManyField(Course)

