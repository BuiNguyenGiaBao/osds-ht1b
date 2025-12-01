from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time

gecko_path = r'D:/bt_fox/geckodriver.exe'

options = Options()
options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"
options.headless = False

service = Service(gecko_path)

driver = webdriver.Firefox(service=service, options=options)

driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")

print("Before:\n", driver.page_source)
time.sleep(3)
print("\n\nAfter:\n", driver.page_source)

driver.quit()
