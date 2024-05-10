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

class TestSearch:
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

    def test_search(self, data):
        self.driver.get("https://school.moodledemo.net/my/courses.php")
        self.driver.maximize_window()
        # self.driver.set_window_size(974, 1047)
        print("Testcase", data.get("Testcase"))
        if data.get("Testcase") == "TC-02-02": 
            self.log_out()
            try:
                element = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class=\'usermenu\']"))).text
                resultlogin = element.strip()
                assert resultlogin == data['Expected Login'].replace('\\n', '\n').strip()
                print("Success, Testcase", data.get("Testcase"), "Assertion login passed: User is not login")
            except AssertionError:
                print("Failure, Testcase", data.get("Testcase"), "Assertion login failed: User is login")
                return
        else:
            try:
                element = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class=\'usermenu\']"))).text
                resultlogin = element.strip()
                assert resultlogin != data['Expected Login'].replace('\\n', '\n').strip()
                print("Success, Testcase", data.get("Testcase"), "Assertion login passed: User is login")
            except AssertionError:
                print("Failure, Testcase", data.get("Testcase"), "Assertion login failed: User is not login")
                return
                
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-open > .icon"))).click()
        self.wait.until(EC.element_to_be_clickable((By.NAME, "q"))).send_keys(data.get("Input"))
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id=\'searchform-navbar\']/form/div/div/button/i"))).click()
        # Handling expected result 1
        if data.get("Testcase") == "TC-02-04":
            try:
                element = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='alert alert-info alert-block fade in  alert-dismissible']"))).text
                result1 = element.strip()
                assert result1 == data['Expected Result 1'].replace("\\\\n", "\n").strip()
                print("Success, Testcase", data.get("Testcase"), "Assertion 1 passed") 
            except AssertionError:
                print("Failure, Testcase", data.get("Testcase"), "Assertion 1 failed") 
            return
        
        try:
            element = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),\'in course Activity Examples\')]"))).text
            result1 = element.strip()
            assert result1 == data['Expected Result 1'].strip()
            print("Success, Testcase", data.get("Testcase"), "Assertion 1 passed")
        except TimeoutException:
            print("Failure, Testcase", data.get("Testcase"), "Assertion 1 failed")
        except AssertionError:
            print("Failure, Testcase", data.get("Testcase"), "Assertion 1 failed")
        
        if data.get("Testcase") == "TC-02-02": 
            self.log_in()
            return
        
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Activity Examples"))).click()
        
        # Handling expected result 2
        try:
            result2 = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".no-overflow > h3"))).text
            assert result2 == data['Expected Result 2']
            print("Success, Testcase", data.get("Testcase"), "Assertion 2 passed")
        except AssertionError:
            print("Failure, Testcase", data.get("Testcase"), "Assertion 2 failed")
        
        
# Read data from Excel file
def read_excel_data(file_path):
    data_frame = pd.read_excel(file_path)
    return data_frame.to_dict(orient='records')

def main():
    test_data = read_excel_data("searchdata.xlsx")
    test = TestSearch(USERNAME, PASSWORD)
    test.log_in()
    
    for data in test_data:
        test.test_search(data)
    
    test.log_out()
    test.driver.quit()

if __name__ == "__main__":
    main()
