from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

# DataFrame kết quả
d = pd.DataFrame({'name': [], 'birth': [], 'death': [], 'nationality': []})

# ------------ HÀM HỖ TRỢ: LẤY INFO TỪ TRANG 1 HOẠ SĨ -----------------
def get_painter_info(driver, url):
    driver.get(url)
    time.sleep(1.5)

    # tên
    try:
        name = driver.find_element(By.ID, "firstHeading").text
    except:
        name = ""

    # ngày sinh
    try:
        birth_element = driver.find_element(
            By.XPATH, "//th[normalize-space()='Born']/following-sibling::td"
        )
        birth_text = birth_element.text
        # lấy dạng "1 January 1900"
        m = re.findall(r"[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{3,4}", birth_text)
        birth = m[0] if m else birth_text.split("\n")[0]
    except:
        birth = ""

    # ngày mất
    try:
        death_element = driver.find_element(
            By.XPATH, "//th[normalize-space()='Died']/following-sibling::td"
        )
        death_text = death_element.text
        m = re.findall(r"[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{3,4}", death_text)
        death = m[0] if m else death_text.split("\n")[0]
    except:
        death = ""

    # quốc tịch
    try:
        nationality_element = driver.find_element(
            By.XPATH, "//th[normalize-space()='Nationality']/following-sibling::td"
        )
        nationality = nationality_element.text.split("\n")[0]
    except:
        nationality = ""

    return {
        "name": name,
        "birth": birth,
        "death": death,
        "nationality": nationality,
    }


# ------------------ MAIN SCRAPER -----------------------
driver = webdriver.Chrome()

all_links = set()

# vòng chữ cái A..Z (demo: A–C, muốn full thì Z + 1)
for i in range(ord("A"), ord("C") + 1):
    list_url = (
        f'https://en.wikipedia.org/wiki/'
        f'List_of_painters_by_name_beginning_with_%22{chr(i)}%22'
    )
    print("Đang lấy links ở:", list_url)
    driver.get(list_url)
    time.sleep(2)

    # các <li> trong nội dung bài viết
    li_tags = driver.find_elements(
        By.CSS_SELECTOR, "div.mw-parser-output > ul > li"
    )

    for li in li_tags:
        try:
            a = li.find_element(By.TAG_NAME, "a")
            href = a.get_attribute("href")
            # chỉ lấy link wiki artist, bỏ các link list khác
            if (
                href
                and href.startswith("https://en.wikipedia.org/wiki/")
                and "List_of_painters_by_name_beginning_with" not in href
                and ":" not in href  # bỏ các namespace đặc biệt
            ):
                all_links.add(href)
        except:
            pass

print("Tổng số link hoạ sĩ lấy được:", len(all_links))

# Lấy thông tin từng hoạ sĩ
for idx, link in enumerate(list(all_links)):
    if idx >= 50:      # giới hạn cho nhẹ, bỏ dòng này nếu muốn lấy hết
        break
    print(idx + 1, "/", len(all_links), "->", link)
    try:
        painter = get_painter_info(driver, link)
        d = pd.concat([d, pd.DataFrame([painter])], ignore_index=True)
    except Exception as e:
        print("Lỗi với link:", link, e)

driver.quit()

print(d.head())

