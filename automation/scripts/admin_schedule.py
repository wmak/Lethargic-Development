#!/usr/bin/env python
# encoding: utf-8
from saunter.testcase.webdriver import SaunterTestCase
from pages.admin.schedule import AdminSchedulePage

import pytest

class CheckAdminSchedulePage(SaunterTestCase):    
	@pytest.marks('regression')
	def test_valid_random_cityname(self):
		admin = AdminSchedulePage(self.driver).open()