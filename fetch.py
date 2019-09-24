from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from page_objects.library import Library
import subprocess
import os
import sys
    
    
        
def handler(event, context):
    #Move executables into /tmp (AWS Lambda is read-only except in /tmp)
    subprocess.check_output('cp ./chromedriver /tmp; cp ./headless-chromium /tmp; chmod 777 /tmp/chromedriver; chmod 777 /tmp/headless-chromium', shell=True, stderr=subprocess.STDOUT)
    #Append chromedriver path to PATH variable
    sys.path.append('/tmp/chromedriver')

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
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = '/tmp/headless-chromium'
    driver = webdriver.Chrome(options=chrome_options, executable_path='/tmp/chromedriver')
    library = Library(driver)
    
    #Start fetching library study room timetables
    driver.get(library.url)
    library.get_room_schedule(0)
    library.get_room_schedule(1)
    library.get_room_schedule(2)
    library.get_room_schedule(3)
    library.get_room_schedule(4)
    library.get_room_schedule(5)
    library.get_room_schedule(6)
    library.get_room_schedule(7)
    library.get_room_schedule(8)
    library.get_room_schedule(9)
    library.get_room_schedule(10)
    driver.quit()
    
    return 'Timetable fetch success.'