from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Edge()
driver.get('https://popcat.click/')
time.sleep(5)
try:
    while True:
        driver.find_element(By.TAG_NAME, 'body').click()
        time.sleep(0.01)
except:
    driver.quit()        



