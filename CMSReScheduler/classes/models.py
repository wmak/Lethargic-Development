from django.db import models

# Create your models here.

class Department(models.Model):
	name = models.CharField(max_length=30)
	numberOfLecturers = models.IntegerField()

	def __unicode__(self):
		return self.name


class Course(models.Model):
	''' We need to have a "day", "start_time", and "end_time"  field for the courses so that we can pass
    them to the front end to use to actually move the schedule around I think.
	'''

	'''
	Ives: we could do that, but the problem here is that there are courses that have lectures, tutorials and practical
	sessions in different days and hours, so for each of them we would have to insert a tuple in the database, and these 
	tuples would have a lot of repeated info (code, name, enrolment, dept). Besides, code is a candidate key for the Course table,
	so it should not be repeated.
	'''
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

class Chair(Instructor):				#incomplete
	
	def prohibitChanges():
		#TODO
		return

	def viewDepartmentCourses():
		return Course.objects.filter(department = self.department)

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

'''
class Schedule(models.Model):
 I don't understand how this one works. A schedule should have all the courses an instructor
    has not just one I think. Also, it should have the day and their start and end times no? I think this would be easier to 
    implement in the courses model.



	Ives: I agree, this one is not very clear. My idea here was that this is like a schedule "item",
	like a cell in a table. But it has some unnecessary information and it does not include days nor the type of session (LEC, TUT or PRA).


	instructor = models.ForeignKey(Instructor)
	course = models.ForeignKey(Course)
	room = models.ForeignKey(Room)
	startTime = models.TimeField()
	endTime = models.TimeField();

	def __unicode__(self):
		return u'%s\n%s\n%s\n%s - %s' % (self.room.code, self.course.code, self.instructor.name, startTime, endTime);
'''


'''Based on Shai's comments, I had another idea of how to represent the Schedule.
   If we do the schedule by course, we avoid repeating info and we can clearly settle the days and hours.
   It should also be somehow high-level, since we can have basically two types of schedules: an instructor's schedule
   and a room's schedule. 
'''
class CourseSchedule(models.Model):
	course = models.ForeignKey(Course)
	room = models.ForeignKey(Room)
	dayOfWeek = models.CharField(max_length = 9)
	startTime = models.TimeField()
	endTime = models.TimeField()
	typeOfSession = models.CharField(max_length = 3) # LEC, TUT or PRA

''' For an instructor's schedule: get instructor.myCourses. For each course in myCourses, use the table above the
								  get its schedule. This is done in getSchedule method in the Instructor class.
	For a room's schedule: filter the table above using room. This is done in getSchedule method in the Room class.
'''

'''
