from pygments.formatters.html import webify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

d = pd.DataFrame({'name': [], 'birth': [], 'death': [], 'nationality': []})
driver = webdriver.Edge()          
url = "https://en.wikipedia.org/wiki/Adolf_Hitler"
driver.get(url)
time.sleep(2)


# Lấy tên hoạ sĩ
try:
    name = driver.find_element(By.TAG_NAME, "h1").text
except:
    name = ""

# Lấy ngày sinh
try:
    birth_element = driver.find_element(
        By.XPATH, "//th[text()='Born']/following-sibling::td"
    )
    birth = birth_element.text
    birth = re.findall(r"[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}", birth)[0]  
except:
    birth = ""

# Lấy ngày mất
try:
    death_element = driver.find_element(
        By.XPATH, "//th[text()='Died']/following-sibling::td"
    )
    death = death_element.text
    death = re.findall(r"[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}", death)[0]
except:
    death = ""

# Lấy quốc tịch
try:
    nationality_element = driver.find_element(
        By.XPATH, "//th[text()='Nationality']/following-sibling::td"
    )
    nationality = nationality_element.text
except:
    nationality = ""

# Tạo dictionary thông tin của hoạ sĩ
painter = {"name": name,"birth": birth,"death": death,"nationality": nationality,}

# Chuyển dictionary thành DataFrame
painter_df = pd.DataFrame([painter])

# Thêm thông tin vào DF chính
d = pd.concat([d, painter_df], ignore_index=True)

print(d)
driver.quit()
