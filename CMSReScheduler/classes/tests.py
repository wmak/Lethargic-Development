"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models.py import *


# Model Testing 

class DepartmentTest(TestCase):
	def setUp(self):
		Department.objects.create_department('Computer Science', 13)

	def test_setUp(self):
		comp_sci = Department.objects.get(name="Computer Science")
		self.assertEqual(comp_sci.name, 'Computer Science')
		self.assertEqual(comp_sci.numberOfLecturers, 13)

	def test_string(self):
		comp_sci = Department.objects.get(name="Computer Science")
		self.assertEqual(comp_sci, 'Computer Science')


class CourseTest(TestCase):
	def setUp(self):
		Course.objects.create_course('Introduction to Software Engineering', 'cscc01h3', 200, 'Coputter Science')

	def test_setUp(self):
		course = Course.objects.get(code="cscc01h3")
		self.assertEqual(course.code, 'cscc01h3')
		self.assertEqual(course.name, 'Introduction to Software Engineering')
		self.assertEqual(course.enrolment, 200)
		self.assertEqual(course.department, 'Computer Science')

	def test_string(self):
		course = Course.objects.get(code="cscc01h3")
		self.assertEqual(course, 'cscc01h3 - Introduction to Software Engineering')


class RoomTest(TestCase):
	def setUp(self):
		Room.objects.create_course('IC220', 150)

	def test_setUp(self):
		room = Room.objects.get(code="IC220")
		self.assertEqual(room.code, 'IC220')
		self.assertEqual(room.capacity, 150)

	def test_string(self):
		room = Room.objects.get(code="IC220")
		self.assertEqual(room, 'IC220')


class UserTest(TestCase):
	def setUp(self):
		User.objects.create_course('Shai Mitchell', '1295 Military Trail, Scarborough, Ontarro', \
			'shai.mitchell@email.ca', 'Coputter Science')

	def test_setUp(self):
		user = Course.objects.get(name="Shai Mitchell")
		self.assertEqual(user.name, 'Shai Mitchell')
		self.assertEqual(user.address, '1295 Military Trail, Scarborough, Ontarro')
		self.assertEqual(user.email, 'shai.mitchell@email.ca')
		self.assertEqual(user.department, 'Computer Science')
		
	def test_string(self):
		user = Course.objects.get(name="Shai Mitchell")
		self.assertEqual(user, 'Shai Mitchell')


# End Of Model Testing
