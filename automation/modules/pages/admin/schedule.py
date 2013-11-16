#!/usr/bin/env python
from saunter.po.webdriver.page import Page
from saunter.ConfigWrapper import ConfigWrapper as cfg_wrapper

locators = {
}

class AdminSchedulePage(Page):
	def __init__(self, driver):
		self.driver = driver
		self.config = cfg_wrapper().config

	def open(self):
		self.driver.get("%s/admin/" % self.config.get("Selenium", "base_url"))
		return self	
