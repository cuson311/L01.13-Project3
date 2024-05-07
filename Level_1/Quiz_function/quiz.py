from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

USERNAME = 'student'
PASSWORD = 'moodle'
COURSE_NAME = 'Cross-cultural Communication'
QUIZ_NAME = 'Cultural Dimensions formative quiz.'

class TestStudentQuiz:
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

    def test_quiz(self, data):
        self.driver.get("https://school.moodledemo.net/my/courses.php")
        self.driver.maximize_window()
        # self.driver.set_window_size(974, 1047)
        self.enter_course(COURSE_NAME)
        if data.get("Testcase") == 'TC-01-01':
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'stretched-link') and .//span[contains(@class, 'instancename') and contains(text(), 'Geert Hoofstede 6-D Model')]]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, COURSE_NAME))).click()
            print("Done the previous Assignment (precondition)")
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, QUIZ_NAME))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//form/button"))).click()
        print("Testcase", data.get("Testcase"))
        # Answer questions based on data from the Excel file
        for question, answer in data.items():
            if question != 'Testcase' and question != 'Expected Result 1' and question != 'Expected Result 2' and answer != "Blank":
                if question == "4.1": question = '4'
                elif question == '8.1': question = '8'
                elif question == '10.1': question = '10'
                # self.driver.find_element(By.XPATH, f"//div[contains(@id, '{question}_')]/div[contains(text(), '{answer}')]").click()
                self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@id, '{question}_')]/div[contains(text(), '{answer}')]"))).click()
        
        # Clicking the next button without waiting for element to be clickable
        self.wait.until(EC.element_to_be_clickable((By.ID, "mod_quiz-next-nav"))).click()
        # self.driver.find_element(By.ID, "mod_quiz-next-nav").click()
        
        # Waiting for the submit button to be clickable
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Submit all and finish')]"))).click()
        
        # Handling expected result 1
        try:
            element = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='quiz-submission-confirmation-content']"))).text
            result1 = element.strip()
            assert result1 == data['Expected Result 1'].replace('\\n', '\n').strip()
            print("Success, Testcase", data.get("Testcase"), "Assertion 1 passed")
        except AssertionError:
            print("Failure, Testcase", data.get("Testcase"), "Assertion 1 failed")
        
        # Clicking the submit button without waiting for it to be clickable
        self.driver.find_element(By.CSS_SELECTOR, ".modal-footer > .btn-primary").click()
        

        # Handling expected result 2
        try:
            result2 = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "tr:nth-child(5) > .cell:nth-child(2)"))).text
            assert result2 == data['Expected Result 2']
            print("Success, Testcase", data.get("Testcase"), "Assertion 2 passed")
        except AssertionError:
            print("Failure, Testcase", data.get("Testcase"), "Assertion 2 failed")

# Read data from Excel file
def read_excel_data(file_path):
    data_frame = pd.read_excel(file_path)
    return data_frame.to_dict(orient='records')

def main():
    test_data = read_excel_data("quizdata.xlsx")
    test = TestStudentQuiz(USERNAME, PASSWORD)
    test.log_in()
    
    for data in test_data:
        test.test_quiz(data)
    
    test.log_out()
    test.driver.quit()

if __name__ == "__main__":
    main()
