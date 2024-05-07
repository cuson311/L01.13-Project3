from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
import pandas as pd

USERNAME = 'student'
PASSWORD = 'moodle'
COURSE_NAME = 'History: Russia in Revolution'
ASSIGNMENT_NAME = 'Assignment: Causes of the October 1917 Revolution'

class TestUpload:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)  # Increased wait time to 20 seconds
        
    def log_in(self):
        self.driver.get('https://school.moodledemo.net/')
        # self.driver.set_window_size(974, 1047)
        self.driver.maximize_window()
        # click log in button
        log_in_button = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Log in')))
        log_in_button.click()
        # get input element
        username_input = self.wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
        password_input =  self.wait.until(EC.visibility_of_element_located((By.NAME, 'password')))
        username_input.clear()
        # fill in the input and submit
        username_input.send_keys(self.username)
        password_input.send_keys(self.password + Keys.ENTER)
        time.sleep(3)
    
    def log_out(self):
        self.driver.get("https://school.moodledemo.net/my/courses.php")
        menu_toggle_element = self.wait.until(EC.element_to_be_clickable((By.ID, 'user-menu-toggle')))
        menu_toggle_element.click()
        log_out_button = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Log out')))
        log_out_button.click()
        time.sleep(3)

    def enter_course(self, course_name):
        course_element = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, course_name)))
        course_element.click()
        
    def test_upload(self, data):
        self.driver.get("https://school.moodledemo.net/my/courses.php")
        self.driver.maximize_window()
        # self.driver.set_window_size(974, 1047)
        self.enter_course(COURSE_NAME)
        print("Testcase", data.get("Testcase"))
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, ASSIGNMENT_NAME))).click()
        #Remove submission
        if data.get("Testcase") == "TC-03-01" or data.get("Testcase") == "TC-03-02":
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),\'Remove submission\')]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),\'Continue\')]"))).click()
        # Add submission
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),\'Add submission\')]"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class=\'fp-btn-add\']/a[@title=\'Add...\']"))).click()
        
        # self.wait.until(EC.visibility_of_element_located((By.NAME, "repo_upload_file"))).click()
        self.wait.until(EC.visibility_of_element_located((By.NAME, "repo_upload_file"))).send_keys(data.get("File"))
        
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),\'Upload this file\')]"))).click()
        
        #Handling expected results
        if data.get("Testcase") == "TC-03-01":
            self.wait.until(EC.element_to_be_clickable((By.ID, "id_submitbutton"))).click()
            try:
                element = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//td[@class=\'submissionstatussubmitted cell c1 lastcol\']"))).text
                result = element.strip()
                assert result == data.get("Expected Result").strip()
                print("Success, Testcase", data.get("Testcase"), "Assertion passed")
            except:
                print("Failure, Testcase", data.get("Testcase"), "Assertion failed")
            return   

        try:
            element = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class=\'moodle-exception-message\']"))).text
            result = element.strip()
            assert result == data.get("Expected Result").strip()
            print("Success, Testcase", data.get("Testcase"), "Assertion passed")
        except:
            print("Failure, Testcase", data.get("Testcase"), "Assertion failed")
        
        
# Read data from Excel file
def read_excel_data(file_path):
    data_frame = pd.read_excel(file_path)
    return data_frame.to_dict(orient='records')

def main():
    test_data = read_excel_data("uploaddata.xlsx")
    test = TestUpload(USERNAME, PASSWORD)
    test.log_in()
    
    for data in test_data:
        test.test_upload(data)
    
    test.log_out()
    test.driver.quit()

if __name__ == "__main__":
    main()
