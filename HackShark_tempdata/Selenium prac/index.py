import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the path to the ChromeDriver executable
webdriver_path = "C:\Drivers\chromedriver_win32\chromedriver.exe"

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(executable_path=webdriver_path)

# Open the IEEE Xplore website
url = 'https://ieeexplore.ieee.org/search/searchresult.jsp?contentType=periodicals&highlight=true&returnType=SEARCH&matchPubs=true&openAccess=true&rowsPerPage=100&pageNumber=20&refinements=ContentType:Journals&returnFacets=ALL'
driver.get(url)

# Wait for the export button to be clickable
export_button_text = 'Export'
export_button_xpath = f"//button[contains(@class, 'xpl-toggle-btn') and contains(text(), '{export_button_text}')]"
export_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, export_button_xpath)))

# Click the export button
export_button.click()

time.sleep(100)
driver.close()