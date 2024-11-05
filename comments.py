from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from configparser import ConfigParser

import signal
import time
import random
import os

# chrome handling
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--log-level=3")  # minimize logging
chrome_service = ChromeService(ChromeDriverManager().install(), log_path=os.devnull)  # suppress logs
chrome = webdriver.Chrome(service=chrome_service, options=chrome_options)

# xpaths 
COOKIE_XPATH = '/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]'
# USERNAME_XPATH = '//*[@id="loginForm"]/div/div[1]/div/label/input'
# PASS_XPATH = '//*[@id="loginForm"]/div/div[2]/div/label/input'
LOGIN_XPATH = '//*[@id="loginForm"]/div/div[3]/button'
# LOGGED_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div'
LOGGED_XPATH = '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div[1]/div/span/div/a'
COMMENT_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div/div[4]/section/div/form/div/textarea'
POST_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div/div[4]/section/div/form/div/div[2]/div'

# colors
RESET = '\033[0m'
GREEN = '\033[32m'
BLUE  = '\033[34m'
RED   = '\033[31m'

# select random names to tag from InfoTag.ini
def choose_names_to_tag(ig_names, required_tags):
    tags = []

    while len(tags) < int(required_tags):
        name = random.choice(ig_names)

        if name not in tags:
            tags.append(name)

    return tags

# script terminating when Ctrl+C
def signal_handler(*args):
    print(f"\n[{RED}X{RESET}] Pressed Ctrl + C")
    print(f"\n[{BLUE}-{RESET}] Script is Terminating...")
    print("-----------------------------")
    exit(69)

if __name__ == "__main__":
    number_of_tags = 0
    tags_limit = 50
    signal.signal(signal.SIGINT, signal_handler)

    os.system('cls')
    print("-----------------------------")
    print(f"[{BLUE}-{RESET}] Script is starting...")

    # open InfoTag.ini
    parser = ConfigParser()
    parser.read('InfoTag.ini', encoding='utf8')

    # gather information from InfoTag.ini
    contest_url = parser.get('Instagram', 'Contest')
    ig_names = parser.get('Instagram', 'Names').replace('\n', '').split(',')
    required_tags = parser.get('Instagram', 'Tags')
    username = parser.get('Instagram', 'Username')
    password = parser.get('Instagram', 'Password')

    # open Instagram
    chrome.get("https://www.instagram.com")
    print(f"\n[{GREEN}-{RESET}] Opened Instagram.")

    try:
        # Wait for cookie acceptance button and click it
        WebDriverWait(chrome, 5).until(EC.presence_of_element_located((By.XPATH, COOKIE_XPATH)))
        cookie_accept = chrome.find_element(By.XPATH, COOKIE_XPATH)
        cookie_accept.click()
        print(f"[{GREEN}-{RESET}] Cookies Accepted.")

        # Wait for username, password, and login button fields to load
        WebDriverWait(chrome, 5).until(EC.presence_of_element_located((By.NAME, "username")))
        username_input = chrome.find_element(By.NAME, "username")
        password_input = chrome.find_element(By.NAME, "password")
        login_button = chrome.find_element(By.XPATH, LOGIN_XPATH)
        print(f"[{GREEN}-{RESET}] Found login elements.")
    except Exception as e:
        # if an error occurs, print a message and terminate the script
        print(f"[{RED}x{RESET}] Failed to find an essential element.")
        exit(69)

    # Proceed with login if elements were successfully found
    username_input.send_keys(username)
    password_input.send_keys(password)

    time.sleep(2)
    login_button.click()

    try:
        # attempt to understand if login is successful
        WebDriverWait(chrome, 15).until(EC.presence_of_element_located((By.XPATH, LOGGED_XPATH)))
        print(f"[{GREEN}-{RESET}] Logged in.")
    except Exception as e:
        # if an error occurs, print a message and terminate the script
        print(f"[{RED}x{RESET}] Failed to log in. \n{str(e).splitlines()[0]}")
        exit(69)

    # goes to the contest post
    chrome.get(contest_url)

    try:
        # attempt to find the comment text area
        WebDriverWait(chrome, 15).until(EC.presence_of_element_located((By.XPATH, COMMENT_XPATH)))
        print(f"[{GREEN}-{RESET}] Found comment section.")
    except Exception as e:
        # if an error occurs, print a message and terminate the script
        print(f"[{RED}x{RESET}] Failed to find comment section. \n{str(e).splitlines()[0]}")
        exit(69)
    
    print(f"\n[{GREEN}>{RESET}] Starting comments.")

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

                # set a random waiting time to avoid block
                seconds_to_wait = random.randint(1,15)
                print("\n\tTagged: {}".format(comment))
                print("\tTotal tags made: {}/{}".format(number_of_tags, tags_limit))
                time.sleep(seconds_to_wait)

                if number_of_tags > (tags_limit-1): # change it as you wish
                    print(f"\n[{RED}x{RESET}] Reached daily comment limit")
                    print(f"\n[{BLUE}-{RESET}] Script is Terminating...")
                    print("-----------------------------")
                    exit(69)
