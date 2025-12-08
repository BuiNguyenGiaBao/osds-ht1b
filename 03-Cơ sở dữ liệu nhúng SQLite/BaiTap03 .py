import os, sqlite3, time, random
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

DB_FILE = r"D:/btsqlite/NHA_THUOC_LONG_CHAU"
TABLE_NAME = "VITAMIN"

print("DB path:", os.path.abspath(DB_FILE))

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print("Đã xoá DB cũ")

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    MA_SP  TEXT PRIMARY KEY,
    TEN_SP TEXT,
    GIA_BAN REAL,
    GIA_GOC REAL,
    DVT    TEXT,
    URL    TEXT
);
""")
conn.commit()
print("Đã tạo bảng xong")

gecko_path = r"D:/osds-ht1b/02-Thu thập dữ liệu với Selenium/BaiTap/bt_fox/geckodriver.exe"
firefox_bin = r"C:/Program Files/Mozilla Firefox/firefox.exe"
url = "https://nhathuoclongchau.com.vn/thuc-pham-chuc-nang/vitamin-khoang-chat"

service = Service(gecko_path)
options = webdriver.FirefoxOptions()
options.binary_location = firefox_bin


driver = webdriver.Firefox(service=service, options=options)

def clean_price(t):
    return t.replace("đ", "").replace(".", "").strip() if t else ""

try:
    driver.get(url)
    time.sleep(5)

    body = driver.find_element(By.TAG_NAME, "body")

    # click "Xem thêm"
    for _ in range(12):
        try:
            btn = driver.find_element(By.XPATH, "//button[.='Xem thêm']")
            btn.click()
            time.sleep(random.uniform(1.5, 3))
        except:
            break

    # scroll
    for _ in range(150):
        body.send_keys(Keys.ARROW_DOWN)
        time.sleep(random.uniform(0.3, 1.2))
    time.sleep(2)

    # lấy link sản phẩm
    buttons = driver.find_elements(By.XPATH, "//button[text()='Chọn mua']")
    print("Tìm thấy sản phẩm:", len(buttons))

    product_links = set()
    for bt in buttons:
        parent = bt
        for _ in range(3):
            parent = parent.find_element(By.XPATH, "./..")
        try:
            link = parent.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            if link:
                product_links.add(link)
        except:
            pass

    product_links = list(product_links)
    print("Số link duy nhất:", len(product_links))

    # cào từng trang
    for link in product_links:
        driver.get(link)
        time.sleep(random.uniform(1.5, 3))

        try: code = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='sku']").text
        except: code = ""

        try: name = driver.find_element(By.TAG_NAME, "h1").text
        except: name = ""

        try: price_sale = clean_price(driver.find_element(By.CSS_SELECTOR, "span[data-test='price']").text)
        except: price_sale = ""

        try: price_old = clean_price(driver.find_element(By.CSS_SELECTOR, "div[data-test='strike_price']").text)
        except: price_old = price_sale

        try: unit = driver.find_element(By.CSS_SELECTOR, "[data-test='unit_lv1']").text.split()[0]
        except: unit = ""

        print("✔", name)

        cursor.execute(
            f"INSERT OR REPLACE INTO {TABLE_NAME} (MA_SP, TEN_SP, GIA_BAN, GIA_GOC, DVT, URL) VALUES (?, ?, ?, ?, ?, ?)",
            (code, name, price_sale, price_old, unit, link)
        )
        conn.commit()

finally:
    driver.quit()
    conn.close()
    print("Đã đóng driver & DB")

print(" kiểm tra file:", os.path.abspath(DB_FILE))


DB_FILE = "NHA_THUOC_LONG_CHAU"
TABLE_NAME = "VITAMIN"

# MỞ KẾT NỐI MỚI
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

print("1. Tổng số sản phẩm trong bảng:")
sql1 = f"SELECT COUNT(*) FROM {TABLE_NAME}"
cursor.execute(sql1)
total_products = cursor.fetchone()[0]
print("  → Tổng số sản phẩm:", total_products)


# 2. Hiển thị 5 dòng dữ liệu đầu tiên để kiểm tra cấu trúc và nội dung bảng.
print("\n2. 5 dòng dữ liệu đầu tiên:")
sql2 = f"SELECT * FROM {TABLE_NAME} LIMIT 5"
cursor.execute(sql2)
rows = cursor.fetchall()
for row in rows:
    ma_sp, ten_sp, gia_ban, gia_goc, dvt, url = row
    print(f"  Mã: {ma_sp} | Tên: {ten_sp} | Giá bán: {gia_ban} | Giá gốc: {gia_goc} | ĐVT: {dvt} | URL: {url}")

# 3. Liệt kê danh sách các đơn vị tính (DVT) duy nhất có trong tập dữ liệu.
print("\n3. Các đơn vị tính (DVT) duy nhất:")
sql3 = f"""
SELECT DISTINCT DVT
FROM {TABLE_NAME}
WHERE DVT IS NOT NULL AND DVT <> ''
"""
cursor.execute(sql3)
rows = cursor.fetchall()
for (dvt,) in rows:
    print("  -", dvt)



# 4. Kiểm tra trùng lặp dựa trên URL (nhóm URL và số lần xuất hiện).
print("\n4. Các URL sản phẩm bị trùng (URL, số bản ghi):")
sql4 = f"""
SELECT URL, COUNT(*) AS cnt
FROM {TABLE_NAME}
GROUP BY URL
HAVING URL IS NOT NULL
   AND URL <> ''
   AND COUNT(*) > 1
"""
cursor.execute(sql4)
rows = cursor.fetchall()
for url, cnt in rows:
    print(f"  - {url} : {cnt} bản ghi")

# 5. Hiển thị đầy đủ bản ghi có URL trùng lặp.
print("\n5. Chi tiết các bản ghi có URL trùng lặp:")
sql5 = f"""
SELECT *
FROM {TABLE_NAME}
WHERE URL IN (
    SELECT URL
    FROM {TABLE_NAME}
    GROUP BY URL
    HAVING URL IS NOT NULL
       AND URL <> ''
       AND COUNT(*) > 1
)
ORDER BY URL, TEN_SP
"""
cursor.execute(sql5)
rows = cursor.fetchall()
for row in rows:
    ma_sp, ten_sp, gia_ban, gia_goc, dvt, url = row
    print(f"  Mã: {ma_sp} | Tên: {ten_sp} | Giá bán: {gia_ban} | Giá gốc: {gia_goc} | ĐVT: {dvt} | URL: {url}")

# 6. Kiểm tra trùng lặp theo tên sản phẩm (TEN_SP).
print("\n6. Tên sản phẩm bị trùng (TEN_SP, số bản ghi):")
sql6 = f"""
SELECT TEN_SP, COUNT(*) AS cnt
FROM {TABLE_NAME}
GROUP BY TEN_SP
HAVING TEN_SP IS NOT NULL
   AND TEN_SP <> ''
   AND COUNT(*) > 1
"""
cursor.execute(sql6)
rows = cursor.fetchall()
for ten_sp, cnt in rows:
    print(f"  - {ten_sp} : {cnt} bản ghi")

# 7. Đếm số sản phẩm thiếu giá bán (GIA_BAN NULL hoặc 0).
print("\n7. Số sản phẩm thiếu giá bán (GIA_BAN NULL hoặc 0):")
sql7 = f"""
SELECT COUNT(*)
FROM {TABLE_NAME}
WHERE GIA_BAN IS NULL
   OR GIA_BAN = 0
"""
cursor.execute(sql7)
missing_price_count = cursor.fetchone()[0]
print("  → Số sản phẩm thiếu giá:", missing_price_count)

# 8. Tìm sản phẩm có giá bán > giá gốc (logic bất thường).
print("\n8. Sản phẩm có giá bán > giá gốc (bất thường):")
sql8 = f"""
SELECT *
FROM {TABLE_NAME}
WHERE GIA_BAN IS NOT NULL
  AND GIA_GOC IS NOT NULL
  AND GIA_BAN > GIA_GOC
"""
cursor.execute(sql8)
rows = cursor.fetchall()
for row in rows:
    ma_sp, ten_sp, gia_ban, gia_goc, dvt, url = row
    print(f"  Mã: {ma_sp} | Tên: {ten_sp} | Giá bán: {gia_ban} | Giá gốc: {gia_goc}")

# 9. Liệt kê các bản ghi có URL NULL hoặc rỗng.
print("\n9. Bản ghi có URL NULL hoặc rỗng:")
sql9 = f"""
SELECT *
FROM {TABLE_NAME}
WHERE URL IS NULL
   OR URL = ''
"""
cursor.execute(sql9)
rows = cursor.fetchall()
for row in rows:
    ma_sp, ten_sp, gia_ban, gia_goc, dvt, url = row
    print(f"  Mã: {ma_sp} | Tên: {ten_sp} | URL: {url}")




# 10. Top 10 sản phẩm có mức giảm giá (GIA_GOC - GIA_BAN) lớn nhất.
print("\n10. Top 10 sản phẩm giảm giá nhiều nhất (theo số tiền):")
sql10 = f"""
SELECT
    MA_SP,
    TEN_SP,
    GIA_GOC,
    GIA_BAN,
    (GIA_GOC - GIA_BAN) AS so_tien_giam
FROM {TABLE_NAME}
WHERE GIA_GOC IS NOT NULL
  AND GIA_BAN IS NOT NULL
  AND GIA_GOC > GIA_BAN
ORDER BY so_tien_giam DESC
LIMIT 10
"""
cursor.execute(sql10)
rows = cursor.fetchall()
for ma_sp, ten_sp, gia_goc, gia_ban, so_tien_giam in rows:
    print(f"  {ma_sp} | {ten_sp} | Gốc: {gia_goc} | Bán: {gia_ban} | Giảm: {so_tien_giam}")

# 11. Sản phẩm có giá bán cao nhất.
print("\n11. Sản phẩm có giá bán cao nhất:")
sql11 = f"""
SELECT *
FROM {TABLE_NAME}
WHERE GIA_BAN IS NOT NULL
ORDER BY GIA_BAN DESC
LIMIT 1
"""
cursor.execute(sql11)
row = cursor.fetchone()
if row:
    ma_sp, ten_sp, gia_ban, gia_goc, dvt, url = row
    print(f"  Mã: {ma_sp} | Tên: {ten_sp} | Giá bán: {gia_ban} | Giá gốc: {gia_goc}")

# 12. Thống kê số lượng sản phẩm theo từng đơn vị tính (DVT).
print("\n12. Số lượng sản phẩm theo từng đơn vị tính (DVT):")
sql12 = f"""
SELECT 
    CASE 
        WHEN DVT IS NULL OR DVT = '' THEN 'Unknown'
        ELSE DVT
    END AS unit,
    COUNT(*) AS total
FROM {TABLE_NAME}
GROUP BY unit
ORDER BY total DESC
"""
cursor.execute(sql12)
rows = cursor.fetchall()
for unit, total in rows:
    print(f"  - {unit}: {total} sản phẩm")

# 13. Sản phẩm có tên chứa từ khóa 'Vitamin C'.
print("\n13. Sản phẩm có tên chứa 'Vitamin C':")
sql13 = f"""
SELECT *
FROM {TABLE_NAME}
WHERE TEN_SP LIKE '%Vitamin C%'
"""
cursor.execute(sql13)
rows = cursor.fetchall()
for row in rows:
    ma_sp, ten_sp, gia_ban, gia_goc, dvt, url = row
    print(f"  Mã: {ma_sp} | Tên: {ten_sp} | Giá bán: {gia_ban}")

# 14. Liệt kê sản phẩm có giá bán từ 100k đến 200k.
print("\n14. Sản phẩm có giá bán trong khoảng 100.000 - 200.000:")
sql14 = f"""
SELECT *
FROM {TABLE_NAME}
WHERE GIA_BAN IS NOT NULL
  AND GIA_BAN BETWEEN 100000 AND 200000
ORDER BY GIA_BAN
"""
cursor.execute(sql14)
rows = cursor.fetchall()
for row in rows:
    ma_sp, ten_sp, gia_ban, gia_goc, dvt, url = row
    print(f"  Mã: {ma_sp} | Tên: {ten_sp} | Giá bán: {gia_ban}")

# 15. Phân nhóm sản phẩm theo nhóm giá: <50k, 50k-100k, >100k.
print("\n15. Phân bố số sản phẩm theo nhóm giá:")
sql15 = f"""
SELECT
    CASE
        WHEN GIA_BAN < 50000 THEN 'Dưới 50k'
        WHEN GIA_BAN BETWEEN 50000 AND 100000 THEN '50k - 100k'
        ELSE 'Trên 100k'
    END AS nhom_gia,
    COUNT(*) AS so_san_pham
FROM {TABLE_NAME}
WHERE GIA_BAN IS NOT NULL
GROUP BY nhom_gia
"""
cursor.execute(sql15)
rows = cursor.fetchall()
for nhom_gia, so_sp in rows:
    print(f"  - {nhom_gia}: {so_sp} sản phẩm")

# 16. Top 5 sản phẩm có % giảm giá cao nhất.
print("\n16. Top 5 sản phẩm có % giảm giá cao nhất:")
sql16 = f"""
SELECT
    MA_SP,
    TEN_SP,
    GIA_GOC,
    GIA_BAN,
    ROUND((GIA_GOC - GIA_BAN) * 100.0 / GIA_GOC, 2) AS phan_tram_giam
FROM {TABLE_NAME}
WHERE GIA_GOC IS NOT NULL
  AND GIA_BAN IS NOT NULL
  AND GIA_GOC > 0
  AND GIA_GOC > GIA_BAN
ORDER BY phan_tram_giam DESC
LIMIT 5
"""
cursor.execute(sql16)
rows = cursor.fetchall()
for ma_sp, ten_sp, gia_goc, gia_ban, pt in rows:
    print(f"  {ma_sp} | {ten_sp} | Gốc: {gia_goc} | Bán: {gia_ban} | Giảm: {pt}%")

# 17. Câu lệnh xóa bản ghi trùng lặp theo URL 
print("\n17. Câu lệnh DELETE bản ghi trùng theo URL (KHÔNG tự chạy trong script):")
delete_duplicates_sql = f"""
WITH to_keep AS (
    SELECT MIN(rowid) AS keep_id
    FROM {TABLE_NAME}
    WHERE URL IS NOT NULL AND URL <> ''
    GROUP BY URL
)
DELETE FROM {TABLE_NAME}
WHERE rowid NOT IN (SELECT keep_id FROM to_keep)
  AND URL IN (
      SELECT URL
      FROM {TABLE_NAME}
      WHERE URL IS NOT NULL AND URL <> ''
      GROUP BY URL
      HAVING COUNT(*) > 1
  );
"""



conn.close()
print("Hoàn thành các truy vấn phân tích dữ liệu VITAMIN.")


