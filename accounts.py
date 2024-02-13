from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from configparser import ConfigParser
from selenium.webdriver.support.ui import Select

chrome = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

import signal
import time
import os

COOKIE_XPATH = '/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]'
REGISTER_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[2]/span/p/a/span'

EMAIL_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div[4]/div/label/input'
NAME_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div[5]/div/label/input'
USERNAME_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div[6]/div/label/input'
PASSWORD_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div[7]/div/label/input'
NEXT1_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div[8]/div/button'

MONTH_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[1]/div[4]/div/div/span/span[1]/select'
DAY_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[1]/div[4]/div/div/span/span[2]/select'
YEAR_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[1]/div[4]/div/div/span/span[3]/select'
NEXT2_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[1]/div[6]/button'

CODE_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/input'
NEXT3_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div'

# script terminating
def signal_handler(*args):
    print("\nScript is Terminating...")
    print("-----------------------------")
    exit(69)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    os.system('cls')
    print("-----------------------------")
    print("Script is Starting...")

    parser = ConfigParser()
    parser.read('InfoAccount.ini', encoding='utf8')

    # gather information from InfoAccount.ini
    email = parser.get('Instagram', 'Email')
    name = parser.get('Instagram', 'Name')
    username = parser.get('Instagram', 'Username')
    password = parser.get('Instagram', 'Password')
    print("\nStep 1. Collected your data")

    # goes to the instagram
    chrome.get("https://www.instagram.com")

    # accepts cookies and register
    WebDriverWait(chrome, 15).until(EC.presence_of_element_located((By.XPATH, REGISTER_XPATH)))

    cookie_accept = chrome.find_element(By.XPATH, COOKIE_XPATH)
    register_button = chrome.find_element(By.XPATH, REGISTER_XPATH)

    cookie_accept.click()
    print("Step 2. Cookies aceepted")
    time.sleep(2) # wait before register click
    register_button.click()
    print("Step 3. Starting register")

    # completes the register form
    WebDriverWait(chrome, 15).until(EC.presence_of_element_located((By.XPATH, EMAIL_XPATH)))

    email_input = chrome.find_element(By.XPATH, EMAIL_XPATH)
    name_input = chrome.find_element(By.XPATH, NAME_XPATH)
    username_input = chrome.find_element(By.XPATH, USERNAME_XPATH)
    password_input = chrome.find_element(By.XPATH, PASSWORD_XPATH)

    time.sleep(1) # wait before completing the form
    email_input.send_keys(email)
    name_input.send_keys(name)
    username_input.send_keys(username)
    password_input.send_keys(password)
    print("Step 4. Printed your data")

    time.sleep(2) # wait to find the next button
    next1_button = chrome.find_element(By.XPATH, NEXT1_XPATH)
    next1_button.click()

    # completes his birthday
    WebDriverWait(chrome, 15).until(EC.presence_of_element_located((By.XPATH, MONTH_XPATH)))

    month_input = chrome.find_element(By.XPATH, MONTH_XPATH)
    day_input = chrome.find_element(By.XPATH, DAY_XPATH)
    year_input = chrome.find_element(By.XPATH, YEAR_XPATH)

    time.sleep(1) # wait before completing the form
    month_select = Select(month_input)
    month_select.select_by_index(0)

    time.sleep(2) # wait to find the next button
    day_select = Select(day_input)
    day_select.select_by_index(0)

    time.sleep(2) # wait to find the next button
    year_select = Select(year_input)
    year_select.select_by_visible_text('2000')
    print("Step 5. Printed default birth date")

    time.sleep(2) # wait to find the next button
    next2_button = chrome.find_element(By.XPATH, NEXT2_XPATH)
    next2_button.click()

    # completes the verification code
    WebDriverWait(chrome, 15).until(EC.presence_of_element_located((By.XPATH, CODE_XPATH)))

    time.sleep(5) # wait for verification code
    verification_code = input("Step 6. Enter the verification code: ")
    code_input = chrome.find_element(By.XPATH, CODE_XPATH)
    code_input.send_keys(verification_code)

    time.sleep(2) # wait to find the next button
    next3_button = chrome.find_element(By.XPATH, NEXT3_XPATH)
    next3_button.click()
    time.sleep(10) # wait to check the code
    print("Step 7. Account created")
    # you can terminate the code with Ctrl + C
    
    time.sleep(60) # wait in case it crash
    print("\nScript is Terminating...")
    print("-----------------------------")
    exit(69)