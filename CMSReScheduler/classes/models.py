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
	code = models.CharField(max_length=9) #ex. CSCC01H3F
	name = models.CharField(max_length=50)
	enrolment = models.IntegerField()
	department = models.ForeignKey(Department)
	day = models.CharField(max_length=10)
	startTime = models.TimeField()
	endTime = models.TimeField()
        def __unicode__(self):
                return u'%s - %s' % (self.code, self.name)

class Room(models.Model):
        code = models.CharField(max_length=10) #ex. IC220
        capacity = models.IntegerField()

        def __unicode__(self):
                return self.code

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

class Chair(Instructor):				#incomplete
	
	def prohibitChanges():
		#TODO

        def viewDepartmentCourses():
                return Course.objects.filter(department = self.department)

        def viewDepartmentInstructors():
                return Instructor.objects.filter(department = self.department)

        def viewInstructorsSchedules():
                instructors = viewDepartmentInstructors();
                schedules = []
                for i in instructors:
                        schedules.append(Schedule.objects.filter(instructor = i))
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

class Schedule(models.Model):
''' I don't understand how this one works. A schedule should have all the courses an instructor
    has not just one I think. Also, it should have the day and their start and end times no? I think this would be easier to 
    implement in the courses model.
'''
	instructor = models.ForeignKey(Instructor)
	course = models.ForeignKey(Course)
	room = models.ForeignKey(Room)
	# startTime = models.TimeField()
	# endTime = models.TimeField()

	def __unicode__(self):
		return u'%s\n%s\n%s\n%s - %s' % (self.room.code, self.course.code, self.instructor.name);
>>>>>>> parent of 1b5a75e... Changed comments to fix IndentationError
