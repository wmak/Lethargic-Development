#!/usr/bin/env python
# encoding: utf-8
from saunter.testcase.webdriver import SaunterTestCase
from pages.admin.upload import AdminUploadPage

import pytest

class CheckAdminSchedulePage(SaunterTestCase):    
	@pytest.marks('regression')
	def test_type_dropdown_switches_to_schedule(self):
		upload = AdminUploadPage(self.driver).open().validate()
		upload.select_type("Schedule")
		self.matchers.verify_equal(upload.current_type, "Schedule")

	@pytest.marks('regression')
	def test_type_dropdown_switches_to_course(self):
		upload = AdminUploadPage(self.driver).open().validate()
		upload.select_type("Course")
		self.matchers.verify_equal(upload.current_type, "Course")