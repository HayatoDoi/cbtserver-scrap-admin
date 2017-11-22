#/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import time
import threading
import urllib
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

domain = 'localhost'
b64_user = 'admin'
b64_pass = 'admin'
browser_path = '/usr/bin/phantomjs'

def launcherChrome(id):
    browser = webdriver.PhantomJS(executable_path=browser_path)
    browser.get( 'http://' + b64_user + ':' + b64_pass + '@' + domain + '/admin/user/profile.php?id=' + id)
    browser.save_screenshot(id + '_' + datetime.now().strftime("%Y_%m_%d_%H.%M.%S.%f") + ".jpg")

chrome_thread_list = []
response = requests.get('http://' + domain + '/admin/user/', auth=(b64_user, b64_pass))
soup = BeautifulSoup(response.text, 'html.parser')
for tr in soup.body.findAll('tr'):
    if not tr.find('a') == None:
        u = tr.find('a')['href']
        id = urllib.parse.parse_qs(urllib.parse.urlparse(u).query)['id'][0]
        chrome_thread_list.append( threading.Thread(target=launcherChrome,  args=(id,)))
        chrome_thread_list[len(chrome_thread_list) - 1].setDaemon(True)
        chrome_thread_list[len(chrome_thread_list) - 1].start()

time.sleep(60)