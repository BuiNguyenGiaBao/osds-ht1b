from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pygments.formatters.html import webify

driver = webdriver.Edge()
driver.get('https://en.wikipedia.org/wiki/List_of_painters_by_name')
time.sleep(10)

tags=driver.find_elements(By.TAG_NAME, "A")
links=[tag.get_attribute("href") for tag in tags]
for link in links: 
    print(link)
    button=driver.find_element(By.LINK_TEXT, link).click()
time.sleep(5)    
driver.quit()