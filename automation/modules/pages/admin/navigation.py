#!/usr/bin/env python
from saunter.po.webdriver.page import Page
from saunter.ConfigWrapper import ConfigWrapper as cfg_wrapper

locators = {
	"Upload" : '//div[contains(@class, "sidebar")]//a[text()="Upload"]',
}

class AdminNavigationPage(Page):
	def __init__(self, driver):
		self.driver = driver
		self.config = cfg_wrapper().config

	def go_to_upload(self, option):
		from upload import AdminUploadPage
		self.driver.find_element_by_locator(locators["Upload"]).click()
		return AdminUploadPage(self.driver).validate()
