#!/usr/bin/env python
from saunter.po.webdriver.page import Page
from saunter.ConfigWrapper import ConfigWrapper as cfg_wrapper
from navigation import AdminNavigationPage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select

locators = {
	"container" : "css=#admin-upload-form",
	"type dropdown" : 'css=[name="type"]',
	"department" : "css=#department",
}

class AdminUploadPage(AdminNavigationPage):
	def __init__(self, driver):
		self.driver = driver
		self.config = cfg_wrapper().config

	@property
	def current_type(self):
		select = Select(self.driver.find_element_by_locator(locators["type dropdown"]))
		return select.first_selected_option.text

	def open(self):
		self.driver.get("%s/admin/upload" % self.config.get("Selenium", "base_url"))
		return self	

	def validate(self):
		w = WebDriverWait(self.driver, 30)
		w.until(lambda driver: self.driver.is_visible(locators['container']))
		return self

	def select_type(self, schedule_type):
		select = Select(self.driver.find_element_by_locator(locators["type dropdown"]))
		select.select_by_visible_text(schedule_type)