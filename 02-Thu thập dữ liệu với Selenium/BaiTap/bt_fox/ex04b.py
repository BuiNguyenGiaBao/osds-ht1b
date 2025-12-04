from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

gecko_path = r"D:/bt_fox/geckodriver.exe"
service = Service(executable_path=gecko_path)

options = Options()
options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"
options.headless = False  

driver = webdriver.Firefox(service=service, options=options)
wait = WebDriverWait(driver, 10)

try:
    url_reddit = "https://www.reddit.com/r/BatmanArkham/"
    driver.get(url_reddit)

    # Đợi có ít nhất 1 link bài
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[slot='full-post-link']")))

    # Scroll vài lần để load thêm post
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Lấy lại list link sau khi scroll
    post_links = driver.find_elements(By.CSS_SELECTOR, "a[slot='full-post-link']")
    print("Tìm được", len(post_links), "link bài (thô)")

    posts_data = []
    seen_link = set()

    for a in post_links:
        try:
            href = a.get_attribute("href")
            if not href:
                continue

            # Build full link
            if href.startswith("http"):
                link = href
            else:
                link = "https://www.reddit.com" + href

            if link in seen_link:
                continue
            seen_link.add(link)

            # Tiêu đề bài
            title = a.text.strip()
            if not title:
                title = (a.get_attribute("innerText") or "").strip()

            # Tìm container cha (shreddit-post hoặc article)
            post_container = None
            try:
                post_container = a.find_element(By.XPATH, "./ancestor::shreddit-post[1]")
            except Exception:
                try:
                    post_container = a.find_element(By.XPATH, "./ancestor::article[1]")
                except Exception:
                    post_container = None

            # Lấy upvote
            upvotes = ""
            if post_container:
                try:
                    vote_el = post_container.find_element(By.CSS_SELECTOR,"faceplate-number[number]")
                    upvotes = vote_el.text.strip()
                except Exception:
                    upvotes = ""

            posts_data.append({
                "title": title,
                "link": link,
                "upvotes": upvotes
            })

        except Exception as e:
            print("Lỗi với 1 bài:", e)
            continue

    print("Cào được", len(posts_data), "bài hợp lệ")

    # Lưu CSV
    if posts_data:
        df = pd.DataFrame(posts_data)
        df.to_csv("reddit_BatmanArkham_posts.csv",
                  index=False,
                  encoding="utf-8-sig")
        print("Đã lưu CSV:", "reddit_BatmanArkham_posts.csv")
    else:
        print("Không cào được bài nào – có thể selector a[slot='full-post-link'] không match nữa.")

finally:
    driver.quit()
