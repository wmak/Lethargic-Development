#!/usr/bin/env python
from saunter.po.webdriver.page import Page
from saunter.ConfigWrapper import ConfigWrapper as cfg_wrapper
from navigation import AdminNavigationPage
from selenium.webdriver.support.wait import WebDriverWait

locators = {
	"schedule container" : "css=.content.fleft",
	"time slot" : "xpath=//div[contains(@class, 'content')]/div[XVALUE]/div[YVALUE]",
}

class AdminSchedulePage(AdminNavigationPage):
	def __init__(self, driver):
		self.driver = driver
		self.config = cfg_wrapper().config

	def open(self):
		self.driver.get("%s/admin/" % self.config.get("Selenium", "base_url"))
		return self	

	def validate(self):
		w = WebDriverWait(self.driver, 30)
		w.until(lambda driver: self.driver.is_visible(locators['schedule container']))
		return self

	def schedule(self, x, y):
		x = str(x)
		y = str(y)
		locator = locators["time slot"].replace("XVALUE", x).replace("YVALUE", y)
		return self.driver.find_element_by_locator(locator).text
