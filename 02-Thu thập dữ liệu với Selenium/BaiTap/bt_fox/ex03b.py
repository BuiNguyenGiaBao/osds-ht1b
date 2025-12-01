from selenium import webdriver
from selenium.webdriver.firefox.service import Service         
from selenium.webdriver.firefox.options import Options         
from selenium.webdriver.common.by import By
import time

gecko_path = r"D:/bt_fox/geckodriver.exe"

service = Service(executable_path=gecko_path)

options = Options()
options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"
options.headless = False   # hiện giao diện

driver = webdriver.Firefox(service=service, options=options)

url = "http://pythonscraping.com/pages/files/form.html"
driver.get(url)

time.sleep(2)

firstname_input = driver.find_element(By.XPATH, "//input[@name='firstname']")
lastname_input  = driver.find_element(By.XPATH, "//input[@name='lastname']")

firstname_input.send_keys("rondom")
time.sleep(1)
lastname_input.send_keys("hoo lee shee")

time.sleep(2)
button = driver.find_element(By.XPATH, "//input[@type='submit']")
button.click()

time.sleep(5)
driver.quit()
