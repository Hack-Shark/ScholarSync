from selenium import webdriver
from selenium.webdriver.common.by import By

import time

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(
    executable_path='C:\Drivers\chromedriver_win32\chromedriver.exe', chrome_options=options)

try:
    driver.get('https://www.browserstack.com/test-on-the-right-mobile-devices')
    downloadcsv = driver.find_element(By.CLASS_NAME,'icon-csv')
    downloadcsv.click()
    # time.sleep(5)
    driver.close()
except:
    print("Invalid URL")
