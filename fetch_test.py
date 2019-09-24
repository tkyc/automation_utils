from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from page_objects.library import Library
import subprocess
import os
import sys
import json
    
    
        
#Set driver options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1280x1696')
chrome_options.add_argument('--user-data-dir=/tmp/user-data')
chrome_options.add_argument('--hide-scrollbars')
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--log-level=0')
chrome_options.add_argument('--v=99')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--data-path=.')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--homedir=.')
chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
chrome_options.binary_location = './headless-chromium'
driver = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver')
library = Library(driver)

#Start fetching library study room timetables
driver.get(library.url)
schedule = {'rooms': []}

for i in range(0, 11, 1):
    schedule['rooms'].append(library.get_room_schedule(i))

#print(schedule)
with open('schedule.json', 'w') as json_file:
    json.dump(schedule, json_file)

driver.quit()
subprocess.check_output('rm -rf locales; rm -rf chrome_debug.log', shell=True, stderr=subprocess.STDOUT)
print('Fetch complete.')