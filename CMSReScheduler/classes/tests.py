"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models.py import *
from views.py import *
from urls.py import *


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
		self.assertEqual(comp_sci.__unicode__(), 'Computer Science')


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
		self.assertEqual(course.__unicode__(), 'cscc01h3 - Introduction to Software Engineering')


class RoomTest(TestCase):
	def setUp(self):
		Room.objects.create_room('IC220', 150)

	def test_setUp(self):
		room = Room.objects.get(code="IC220")
		self.assertEqual(room.code, 'IC220')
		self.assertEqual(room.capacity, 150)

	def test_string(self):
		room = Room.objects.get(code="IC220")
		self.assertEqual(room.__unicode__(), 'IC220')


class UserTest(TestCase):
	def setUp(self):
		User.objects.create_user('Shai Mitchell', '1295 Military Trail, Scarborough, Ontarro', \
			'shai.mitchell@email.ca', 'Coputter Science')

	def test_setUp(self):
		user = Course.objects.get(name="Shai Mitchell")
		self.assertEqual(user.name, 'Shai Mitchell')
		self.assertEqual(user.address, '1295 Military Trail, Scarborough, Ontarro')
		self.assertEqual(user.email, 'shai.mitchell@email.ca')
		self.assertEqual(user.department, 'Computer Science')
		
	def test_string(self):
		user = Course.objects.get(name="Shai Mitchell")
		self.assertEqual(user.__unicode__(), 'Shai Mitchell')


# End Of Model Testing


# View Testing
class AdminTest(TestCase):
	def test_admin_status(self):
		url = reverse('CMSReScheduler.views.admin')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)

class AdminUploadTest(TestCase):
	def test_admin_upload_status(self):
		url = reverse('CMSReScheduler.views.admin_upload')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)

class CourseTest(TestCase):
	def test_course_cscc01h3_status(self):
		url = '/course/cscc01h3'
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)

class CsvImportTest(object):
	def test_csv_upload_schedule_status(self):
		url = '/csvimport/schedule'
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)

	def test_csv_upload_course_status(self):
		url = '/csvimport/course'
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		

# End of View Testing