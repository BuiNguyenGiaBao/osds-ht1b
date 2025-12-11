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

finally:
    #A. Yêu Cầu Thống Kê và Toàn Cục
    #1. Đếm tổng số họa sĩ đã được lưu trữ trong bảng.
    sql1= f"SELECT COUNT(*) FROM {TABLE_NAME}"
    cursor.execute(sql1)
    total_painters= cursor.fetchone()[0]

    #2. Hiển thị 5 dòng dữ liệu đầu tiên để kiểm tra cấu trúc và nội dung bảng.
    sql2= f"SELECT * FROM {TABLE_NAME} LIMIT 5"
    cursor.execute(sql2)
    rows= cursor.fetchall()

    for row in rows :
        name,birth,death,nationality=row
        print(f"  Tên: {name} | Sinh: {birth} | Mất: {death} | Quốc tịch: {nationality}")

    #3. Liệt kê danh sách các quốc tịch duy nhất có trong tập dữ liệu.
    sql3 = f"""
    SELECT DISTINCT nationality
    FROM {TABLE_NAME}
    WHERE nationality IS NOT NULL AND nationality <> ''
    """
    cursor.execute(sql3)
    rows = cursor.fetchall()
    for (nation,) in rows:
        print("  -", nation)


    #B. Yêu Cầu Lọc và Tìm Kiếm
    #4. Tìm và hiển thị tên của các họa sĩ có tên bắt đầu bằng ký tự 'F'.
    print("\n4. Họa sĩ có tên bắt đầu bằng 'F':")
    sql4 = f"""
    SELECT name
    FROM {TABLE_NAME}
    WHERE name LIKE 'F%'
    """
    cursor.execute(sql4)
    rows = cursor.fetchall()
    for (name,) in rows:
        print("  -", name)

    #5. Tìm và hiển thị tên và quốc tịch của những họa sĩ có quốc tịch chứa từ khóa 'French' (ví dụ: French, French-American).
    print("\n5. Họa sĩ có quốc tịch chứa 'French':")
    sql5 = f"""
    SELECT name, nationality
    FROM {TABLE_NAME}
    WHERE nationality LIKE '%French%'
    """
    cursor.execute(sql5)
    rows = cursor.fetchall()
    for name, nationality in rows:
        print(f"  - {name} ({nationality})")

    #6. Hiển thị tên của các họa sĩ không có thông tin quốc tịch (hoặc để trống, hoặc NULL).
    print("\n6. Họa sĩ không có thông tin quốc tịch:")
    sql6 = f"""
    SELECT name
    FROM {TABLE_NAME}
    WHERE nationality IS NULL OR nationality = ''
    """
    cursor.execute(sql6)
    rows = cursor.fetchall()
    for (name,) in rows:
        print("  -", name)

    #7. Tìm và hiển thị tên của những họa sĩ có cả thông tin ngày sinh và ngày mất (không rỗng).
    print("\n7. Họa sĩ có đủ ngày sinh và ngày mất:")
    sql7 = f"""
    SELECT name
    FROM {TABLE_NAME}
    WHERE birth IS NOT NULL AND birth <> ''
    AND death IS NOT NULL AND death <> ''
    """
    cursor.execute(sql7)
    rows = cursor.fetchall()
    for (name,) in rows:
        print("  -", name)

    #8. Hiển thị tất cả thông tin của họa sĩ có tên chứa từ khóa '%Fales%' (ví dụ: George Fales Baker).
    print("\n8. Thông tin họa sĩ có tên chứa 'Fales':")
    sql8 = f"""
    SELECT *
    FROM {TABLE_NAME}
    WHERE name LIKE '%Fales%'
    """
    cursor.execute(sql8)
    rows = cursor.fetchall()
    for row in rows:
        name, birth, death, nationality = row
        print(f"  Tên: {name} | Sinh: {birth} | Mất: {death} | Quốc tịch: {nationality}")


    #C. Yêu Cầu Nhóm và Sắp Xếp
    #9. Sắp xếp và hiển thị tên của tất cả họa sĩ theo thứ tự bảng chữ cái (A-Z).
    print("\n9. Tên tất cả họa sĩ (A-Z):")
    sql9 = f"""
    SELECT name
    FROM {TABLE_NAME}
    ORDER BY name ASC
    """
    cursor.execute(sql9)
    rows = cursor.fetchall()
    for (name,) in rows:
        print("  -", name)

    #10. Nhóm và đếm số lượng họa sĩ theo từng quốc tịch.
    print("\n10. Số lượng họa sĩ theo quốc tịch:")
    sql10 = f"""
    SELECT 
        CASE 
            WHEN nationality IS NULL OR nationality = '' THEN 'Unknown'
            ELSE nationality
        END AS nation,
        COUNT(*) AS total
    FROM {TABLE_NAME}
    GROUP BY nation
    ORDER BY total DESC
    """
    cursor.execute(sql10)
    rows = cursor.fetchall()
    for nation, total in rows:
        print(f"  - {nation}: {total} họa sĩ")



conn.close()
print("\nĐã đóng kết nối cơ sở dữ liệu.")