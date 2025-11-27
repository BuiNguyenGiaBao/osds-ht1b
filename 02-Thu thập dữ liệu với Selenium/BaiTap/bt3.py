from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver=webdriver.Edge()

driver.get("https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22P%22")
time.sleep(2)

ul_tag=driver.find_elements(By.TAG_NAME,"ul")
print(len(ul_tag))

ul_painter= ul_tag[20]

li_tag= ul_painter.find_elements(By.TAG_NAME, "li")

links = [tag.find_element(By.TAG_NAME,"a").get_attribute('href') for tag in li_tag]
title = [tag.find_element(By.TAG_NAME,"a").get_attribute('title') for tag in li_tag]
for link in links :
    print (link)
for title in title:
    print(title)

driver.quit()