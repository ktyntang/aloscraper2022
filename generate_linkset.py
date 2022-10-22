import socket
import time
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from parse_har import find_url_in_har

socket.setdefaulttimeout(10)

def newbrowser():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    browser = webdriver.Chrome(options=options,seleniumwire_options={'enable_har': True})
    return browser

def doLogin(email, password,browser):
    browser.get("https://www.alomoves.com/signin")
    time.sleep(5)
    mailfield = browser.find_element('xpath', "//input[contains(@name,'email')]")
    pwfield = browser.find_element('xpath', "//input[contains(@name,'password')]")
    mailfield.send_keys(email)
    mailfield.send_keys(Keys.TAB)
    time.sleep(1)
    pwfield.send_keys(password)
    pwfield.send_keys(Keys.ENTER)

def generate_har(link,browser):
    browser.get(link)
    time.sleep(15)
    data = browser.har
    time.sleep(5)
    name = link.split('/')[-1].split('?')[0]
    harfile = str(name) + ".har"
    with open(harfile, "w") as file:
        file.write((data))
    return harfile


def generate_linkset(link, email, password):
    browser = newbrowser()
    doLogin(email, password, browser)
    time.sleep(5)
    videourl = find_url_in_har(generate_har(link, browser))
    videourlHD = videourl.replace('842x480','1280x720')
    browser.get("https://www.alomoves.com/signout")
    time.sleep(3)
    browser.quit()
    return [link,videourlHD]

