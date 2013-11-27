#!/usr/bin/env python
# encoding: utf-8
from saunter.testcase.webdriver import SaunterTestCase
from pages.admin.schedule import AdminSchedulePage

import pytest

class CheckAdminSchedulePage(SaunterTestCase):    
	@pytest.marks('regression')
	def test_schedule_has_Monday(self):
		admin = AdminSchedulePage(self.driver).open().validate()
		self.matchers.verify_equal(admin.schedule(2,1), "Monday")

	@pytest.marks('regression')
	def test_schedule_has_Tuesday(self):
		admin = AdminSchedulePage(self.driver).open().validate()
		self.matchers.verify_equal(admin.schedule(3,1), "Tuesday")

	@pytest.marks('regression')
	def test_schedule_has_Wednesday(self):
		admin = AdminSchedulePage(self.driver).open().validate()
		self.matchers.verify_equal(admin.schedule(4,1), "Wednesday")

	@pytest.marks('regression')
	def test_schedule_has_Thursday(self):
		admin = AdminSchedulePage(self.driver).open().validate()
		self.matchers.verify_equal(admin.schedule(5,1), "Thursday")

	@pytest.marks('regression')
	def test_schedule_has_Friday(self):
		admin = AdminSchedulePage(self.driver).open().validate()
		self.matchers.verify_equal(admin.schedule(6,1), "Friday")
