from selenium import webdriver
from selenium.webdriver.common.by import By
from pygments.formatters.html import HtmlFormatter
import time

driver = webdriver.Chrome()
url = "https://en.wikipedia.org/wiki/list_of_painters_by_name"
driver.get(url)
driver.maximize_window()
time.sleep(5)

tags = driver.find_elements(By.XPATH, "//a[contains(@title, 'List of painters')]")

links = [tag.get_attribute("Href") for tag in tags]

for link in links:
    print(link)
