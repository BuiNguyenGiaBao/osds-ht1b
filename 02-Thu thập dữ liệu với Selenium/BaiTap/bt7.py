from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

start_url = "https://vi.wikipedia.org/wiki/Th%E1%BB%83_lo%E1%BA%A1i:Tr%C6%B0%E1%BB%9Dng_cao_%C4%91%E1%BA%B3ng_t%E1%BA%A1i_Vi%E1%BB%87t_Nam"
max_schools = 54   

driver = webdriver.Edge()

all_school_links = []

try:
    driver.get(start_url)
    time.sleep(3)

    # Khu vực liệt kê trang trong thể loại (mw-pages)
    a_tags = driver.find_elements(By.CSS_SELECTOR, "#mw-pages .mw-category-group ul li a")

    for a in a_tags:
        href = a.get_attribute("href")
        if not href:
            continue

        # Chỉ lấy bài viết bình thường trên vi.wikipedia
        if not href.startswith("https://vi.wikipedia.org/wiki/"):
            continue

        # Bỏ các trang kiểu Thành_viên:, Thể_loại:, Wikipedia:, File: ...
        title_part = href.split("/wiki/")[1]
        if ":" in title_part:
            continue

        if href not in all_school_links:
            all_school_links.append(href)

        if len(all_school_links) >= max_schools:
            break

    print("Số link trường lấy được:", len(all_school_links))

    records = []

    for idx, link in enumerate(all_school_links, start=1):
        print(f"[{idx}/{len(all_school_links)}] Đang xử lý:", link)
        driver.get(link)
        time.sleep(2)

        # Tên trường: tiêu đề lớn trên cùng
        try:
            school_name = driver.find_element(By.ID, "firstHeading").text.strip()
        except:
            school_name = ""

        # Mặc định nếu không tìm thấy
        ma_truong = ""
        hieu_truong = ""
        website_truong = ""

        # Tìm bảng infobox 
        try:
            infobox_rows = driver.find_elements(By.CSS_SELECTOR, "table.infobox tr")
            for row in infobox_rows:
                try:
                    th = row.find_element(By.TAG_NAME, "th").text.strip()
                    td = row.find_element(By.TAG_NAME, "td")
                    value_text = td.text.strip()
                except:
                    continue

                # Mã trường
                if "Mã trường" in th:
                    ma_truong = value_text

                # Hiệu trưởng
                if "Hiệu trưởng" in th:
                    hieu_truong = value_text

                # Website / Trang web
                if "Website" in th or "Trang web" in th:
                    try:
                        a_website = td.find_element(By.TAG_NAME, "a")
                        website_truong = a_website.get_attribute("href") or value_text
                    except:
                        website_truong = value_text

        except:
            pass

        records.append({
            "tên trường": school_name,
            "mã trường": ma_truong,
            "tên hiệu trưởng": hieu_truong,
            "link web trường": website_truong,
            "link wiki": link, 
        })


    d = pd.DataFrame(records)
    print(d.head())
    d.to_csv("truong_cao_dang_vn.csv", index=False, encoding="utf-8-sig")

finally:
    driver.quit()
