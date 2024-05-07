# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestLargefile():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_largefile(self):
    self.driver.get("https://school.moodledemo.net/my/courses.php")
    self.driver.set_window_size(1936, 1056)
    self.driver.find_element(By.LINK_TEXT, "History: Russia in Revolution").click()
    self.driver.find_element(By.LINK_TEXT, "Assignment: Causes of the October 1917 Revolution").click()
    self.driver.find_element(By.XPATH, "//button[contains(text(),\'Remove submission\')]").click()
    self.driver.find_element(By.XPATH, "//button[contains(text(),\'Continue\')]").click()
    self.driver.find_element(By.XPATH, "//button[contains(text(),\'Add submission\')]").click()
    self.driver.find_element(By.XPATH, "//div[@class=\'fp-btn-add\']/a[@title=\'Add...\']").click()
    self.driver.find_element(By.NAME, "repo_upload_file").send_keys("C:\\Software-Testing\\5_Unitintergration testing.pdf")
    self.driver.find_element(By.XPATH, "//button[contains(text(),\'Upload this file\')]").click()
    assert self.driver.find_element(By.XPATH, "//div[@class=\'moodle-exception-message\']").text == "The file 5_Unitintergration testing.pdf is too large. The maximum size you can upload is 1 MB."
  
