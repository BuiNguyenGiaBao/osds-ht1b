from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd

gecko_path = r"D:/bt_fox/geckodriver.exe"
ser = Service(gecko_path)

options = webdriver.firefox.options.Options()
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
options.headless = False

driver = webdriver.Firefox(options=options, service=ser)
wait = WebDriverWait(driver, 20)

url = "https://gochek.vn/"
driver.get(url)

def close_wheel_if_present(driver, timeout=10):
    try:
        w = WebDriverWait(driver, timeout)
        close_btn = w.until(EC.element_to_be_clickable((By.ID, "closeWheel")))
        close_btn.click()
        time.sleep(1)  # chờ popup biến mất hẳn
    except TimeoutException:
        pass  # không có popup thì thôi

# 1. Tắt popup nếu có
close_wheel_if_present(driver)

# 2. Thử bấm vào "Sản phẩm"
try:
    san_pham_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sản phẩm")))
    driver.execute_script("arguments[0].click();", san_pham_link)
    print("Đã click vào menu 'Sản phẩm'.")
except TimeoutException:
    print("Không tìm được link 'Sản phẩm', chuyển thẳng vào trang tất cả sản phẩm.")
    driver.get("https://gochek.vn/collections/all")

# 3. Đợi list sản phẩm hiện ra
products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.product-block.product-resize.site-animation.fixheight")))

stt = []
ten_san_pham = []
gia_ban_ban_dau=[]
gia_ban = []
hinh_anh = []

for i, sp in enumerate(products, start=1):
    # Lấy tên sản phẩm
    try:
        tsp = sp.find_element(By.CSS_SELECTOR, "h3.pro-name a").text.strip()
    except:
        tsp = ""

    # Lấy giá (giá đang bán)
    try:
        gsp = sp.find_element(By.CSS_SELECTOR, ".box-pro-prices .pro-price span").text.strip()
    except:
        gsp = ""
    # Lấy giá mặc định 
    try:
        gbd= gsp = sp.find_element(By.CSS_SELECTOR, ".box-pro-prices .compare-price").text.strip()
    except:
        gbd=''       
    # Lấy link hình ảnh
    try:
        ha = sp.find_element(By.CSS_SELECTOR, ".product-img img").get_attribute("src")
    except:
        ha = ""

    if tsp:
        stt.append(i)
        ten_san_pham.append(tsp)
        gia_ban.append(gsp)
        gia_ban_ban_dau.append(gbd)
        hinh_anh.append(ha)

# 4. Tạo DataFrame và lưu Excel
df = pd.DataFrame({
    "STT": stt,
    "Tên sản phẩm": ten_san_pham,
    "Giá bán": gia_ban,
    "Giá ban đầu": gia_ban_ban_dau,
    "Hình ảnh": hinh_anh

})

df.to_excel("danh_sach_sp_3.xlsx", index=False)
print("Đã lưu danh_sach_sp_3.xlsx")

driver.quit()
