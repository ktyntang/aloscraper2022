import socket
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

socket.setdefaulttimeout(10)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')
browser = webdriver.Chrome(options=options)
lines = []
LINKFILE = os.getcwd() + "/downloadlinks.txt"

with open(LINKFILE) as f:
    lines = [line.rstrip() for line in f]
    for line in lines:
        line = line.split("/series")[1].split("workouts")[0]

def doLogin(email, password):
    browser.get("https://www.alomoves.com/signin")
    time.sleep(5)
    mailfield = browser.find_element('xpath', "//input[contains(@name,'email')]")
    pwfield = browser.find_element('xpath', "//input[contains(@name,'password')]")
    mailfield.send_keys(email)
    mailfield.send_keys(Keys.TAB)
    time.sleep(1)
    pwfield.send_keys(password)
    pwfield.send_keys(Keys.ENTER)

def collectClasses(courselink):
    print(f"== Grabbing links for {courselink} ==")
    time.sleep(5)
    browser.get(courselink)
    time.sleep(5)
    workoutLinks = browser.find_elements('xpath',
        "//div[contains(@class,'workout-title')]/a")
    reallinks = [link.get_attribute("href") for link in workoutLinks]
    return reallinks

def getclasslinks(email, password):
    classlinks = []
    doLogin(email, password)
    for i in range(len(lines)):
        classlinks.append(collectClasses(lines[i]))
    browser.quit()
    print("CLASS LINKS COLLECTED")
    return classlinks
