from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from configparser import ConfigParser

chrome = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

import signal
import time
import random
import os

COOKIE_XPATH = '/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]'

USERNAME_XPATH = '//*[@id="loginForm"]/div/div[1]/div/label/input'
PASS_XPATH = '//*[@id="loginForm"]/div/div[2]/div/label/input'

LOGIN_XPATH = '//*[@id="loginForm"]/div/div[3]/button'
LOGGED_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div'

POST_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[4]/section/div/form/div/div[2]/div'
COMMENT_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[4]/section/div/form/div/textarea'

# select random names to tag from InfoTag.ini
def choose_names_to_tag(ig_names, required_tags):
    tags = []

    while len(tags) < int(required_tags):
        name = random.choice(ig_names)

        if name not in tags:
            tags.append(name)

    return tags

# script terminating
def signal_handler(*args):
    print("\nScript is Terminating...")
    print("-----------------------------")
    exit(69)

if __name__ == "__main__":
    number_of_tags = 0
    signal.signal(signal.SIGINT, signal_handler)

    os.system('cls')
    print("-----------------------------")
    print("Script is Starting...")

    parser = ConfigParser()
    parser.read('InfoTag.ini', encoding='utf8')

    # gather information from InfoTag.ini
    contest_url = parser.get('Instagram', 'Contest')
    ig_names = parser.get('Instagram', 'Names').replace('\n', '').split(',')
    required_tags = parser.get('Instagram', 'Tags')
    username = parser.get('Instagram', 'Username')
    password = parser.get('Instagram', 'Password')

    # goes to the instagram
    chrome.get("https://www.instagram.com")

    WebDriverWait(chrome, 15).until(EC.presence_of_element_located((By.XPATH, USERNAME_XPATH)))

    # finds cookies and log in form on the browser
    cookie_accept = chrome.find_element(By.XPATH, COOKIE_XPATH)
    username_input = chrome.find_element(By.XPATH, USERNAME_XPATH)
    password_input = chrome.find_element(By.XPATH, PASS_XPATH)
    login_button = chrome.find_element(By.XPATH, LOGIN_XPATH)

    # accepts cookies and logs the user in
    cookie_accept.click()
    username_input.send_keys(username)
    password_input.send_keys(password)

    time.sleep(2)
    login_button.click()

    WebDriverWait(chrome, 15).until(EC.presence_of_element_located((By.XPATH, LOGGED_XPATH)))

    # goes to the contest post
    chrome.get(contest_url)

    WebDriverWait(chrome, 15).until(EC.presence_of_element_located((By.XPATH, COMMENT_XPATH)))

    while True:
        names = choose_names_to_tag(ig_names, required_tags)
        time.sleep(5)

        # finds the comment input on the post
        comment_input = chrome.find_element(By.XPATH, COMMENT_XPATH)
        comment_input.click()
        comment_input = chrome.find_element(By.XPATH, COMMENT_XPATH)
        
        # types the names
        comment = ""
        for name in names:
            comment += "{} ".format(name)

        # sends the comment
        comment_input.send_keys(comment)
        post_button = chrome.find_element(By.XPATH, POST_XPATH)
        post_button.click()

        time.sleep(2)

        waiting_to_unblock = True

        while waiting_to_unblock:
            try:
                # if element is present then IG blocked comments
                chrome.find_element_by_class_name("HGN2m")
                print("blocked")

                # wait 1 min before commenting again
                time.sleep(60)
                post_button = chrome.find_element(By.XPATH, POST_XPATH).click()
                time.sleep(2)
            except:
                waiting_to_unblock = False
                number_of_tags += 1

                # set a random waiting time to not get blocked
                seconds_to_wait = random.randint(1,15)
                print("\nTagged: {}".format(comment))
                print("Total tags made: {}/120".format(number_of_tags))
                time.sleep(seconds_to_wait)

                if number_of_tags > 119:
                    print("\nReached daily comment limit")
                    print("\nScript is Terminating...")
                    print("-----------------------------")
                    exit(69)
