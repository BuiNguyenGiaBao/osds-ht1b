from builtins import range
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver= webdriver.Edge()
for  i in range (65,91):
        try:
            driver.get(f'https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22{chr(i)}%22')
            time.sleep(3)
            ul_tags= driver.find_elements(By.TAG_NAME, 'ul')
            print(len(ul_tags))
            ul_painter= ul_tags[20]
            li_tag=ul_painter.find_elements(By.TAG_NAME,'li')
            title = [tag.find_element(By.TAG_NAME,"a").get_attribute('title') for tag in li_tag]
            for title in title:
                  print(title)
        except:
              print('erro')          
            
driver.quit()
            