from django.db import models

# Create your models here.

class Department(models.Model):
	name = models.CharField(max_length=30)
	numberOfLecturers = models.IntegerField()

class Course(models.Model):
	code = models.CharField(max_length=9) #ex. CSCC01H3F
	enrolment = models.IntegerField()
	department = models.ForeignKey(Department)

class Room(models.Model):
	code = models.CharField(max_length=10) #ex. IC220
	capacity = models.IntegerField()

class User(models.Model):
	name = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
	email = models.EmailField()
	department = models.ForeignKey(Department)

class Lecturer(User):			#incomplete
	room = models.ForeignKey(Room)

class Chair(User):				#incomplete
	room = models.ForeignKey(Room)

class Schedule(models.Model):
	lecturer = models.ForeignKey(Lecturer)
	course = models.ForeignKey(Course)
	room = models.ForeignKey(Room)