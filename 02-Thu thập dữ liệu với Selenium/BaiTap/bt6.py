import time
import re
import string
import sqlite3
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By


gecko_path = r"D:/bt_fox/geckodriver.exe"  
ser = Service(gecko_path)

options = webdriver.firefox.options.Options()
options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"  
options.headless = False

driver = webdriver.Firefox(service=ser, options=options)

DB_FILE = "Painters_Data.db"
TABLE_NAME = "painters_info"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    name        TEXT PRIMARY KEY,
    birth       TEXT,
    death       TEXT,
    nationality TEXT
)
""")
conn.commit()

MAX_PAINTERS = 300         
LETTERS = list(string.ascii_uppercase)  


BASE_LIST_URL = (
    "https://en.wikipedia.org/wiki/"
    "List_of_painters_by_name_beginning_with_%22{}%22"
)




ROLE_KEYWORDS = [
    "painter", "artist", "sculptor", "print-maker", "etcher",
    "engraver", "photographer", "muralist", "water-colorist",
    "war artist", "calligrapher", "draftsman", "landscape",
]


def split_life(life_str: str):
    """
    Nhận chuỗi trong ngoặc, trả về (birth, death)
    - "1923–1985" -> ("1923", "1985")
    - "born 1960" -> ("1960", "")
    - "4th century BC" -> ("", "")
    """
    if not life_str:
        return "", ""

    # 2 năm (range)
    m = re.search(r"(\d{3,4})\D+(\d{3,4})", life_str)
    if m:
        return m.group(1), m.group(2)

    # 1 năm + chữ born -> còn sống
    m = re.search(r"born[^0-9]*?(\d{3,4})", life_str.lower())
    if m:
        return m.group(1), ""

    # 1 năm đơn lẻ -> cho vào birth, death để trống
    m = re.search(r"(\d{3,4})", life_str)
    if m:
        return m.group(1), ""

    return "", ""


def parse_li(li):
    """
    Parse 1 <li> trên trang list.
    Trả về dict: name, birth, death, nationality
    """
    # 1) Tên lấy từ <a> đầu tiên
    a_tags = li.find_elements(By.TAG_NAME, "a")
    if not a_tags:
        return None

    name = a_tags[0].text.strip()
    if not name:
        return None

    # 2) Chuỗi full text của <li>
    full_text = li.text.strip()

    # Bỏ phần name ở đầu -> tail
    if full_text.startswith(name):
        tail = full_text[len(name):].lstrip(" ,–-")
    else:
        # fallback, nhưng thường không xảy ra
        tail = full_text

    # 3) Lấy life trong ngoặc đầu tiên
    m = re.search(r"\(([^()]*)\)", tail)
    life_str = None
    if m:
        life_str = m.group(1).strip()
        details = tail[m.end():].lstrip(" ,")
    else:
        details = tail

    birth, death = split_life(life_str or "")

    # 4) Lấy nationality từ details
    #    -> đoạn trước từ khóa role (painter/artist/...)
    nationality = ""
    dlow = details.lower()
    best_idx = None
    for role in ROLE_KEYWORDS:
        idx = dlow.find(role)
        if idx != -1:
            if best_idx is None or idx < best_idx:
                best_idx = idx

    if best_idx is not None:
        nationality = details[:best_idx].rstrip(" ,")
    else:
        # nếu không tìm thấy role thì thử lấy trước dấu phẩy đầu tiên
        parts = details.split(",")
        if parts:
            nationality = parts[0].strip()

    return {
        "name": name,
        "birth": birth,
        "death": death,
        "nationality": nationality,
    }

total_crawled = 0
names_seen = set()

try:
    for letter in LETTERS:
        if total_crawled >= MAX_PAINTERS:
            break

        url = BASE_LIST_URL.format(letter)
        print(f"\n=== Đang xử lý trang chữ {letter}: {url}")
        driver.get(url)
        time.sleep(2)

        # Tất cả <li> trong phần nội dung chính
        lis = driver.find_elements(By.CSS_SELECTOR, "div.mw-parser-output > ul > li")
        print(f"  -> Tìm được {len(lis)} dòng <li> cho chữ {letter}")

        for li in lis:
            if total_crawled >= MAX_PAINTERS:
                break

            data = parse_li(li)
            if not data:
                continue

            name = data["name"]
            if name in names_seen:
                continue
            names_seen.add(name)

            # Lưu vào DB
            cursor.execute(
                f"""INSERT OR IGNORE INTO {TABLE_NAME}
                    (name, birth, death, nationality)
                    VALUES (?, ?, ?, ?)""",
                (data["name"], data["birth"], data["death"], data["nationality"]),
            )
            conn.commit()

            total_crawled += 1
            print(
                f"  [{total_crawled}] {data['name']} | "
                f"{data['birth']} - {data['death']} | {data['nationality']}"
            )

    print(f"\nHoàn thành, đã cào tổng cộng: {total_crawled} painter.")