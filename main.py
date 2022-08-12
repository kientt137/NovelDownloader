import mariadb
import sys
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
import re

url = "https://m.yushubo.cc/read_83404_{}.html"
# '2018-05-30 00:00:00'
cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("date and time =", cur_time)

# setup webdriver
path = r'C:\Users\KienTT2\chromedriver_win32\chromedriver.exe'
op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(options=op, executable_path=path)


# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="admin",
        password="Thuong1212",
        host="webtruyen-db.cvgujndmldir.ap-southeast-1.rds.amazonaws.com",
        port=3306,
        database="wp_truyenraw"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

sql_insert = "INSERT INTO wp_truyen_posts (post_author, " \
    "post_date, " \
    "post_date_gmt, " \
    "post_content, " \
    "post_title, " \
    "post_excerpt, " \
    "to_ping, " \
    "pinged, " \
    "post_content_filtered, " \
    "post_status, " \
    "comment_status, " \
    "ping_status, " \
    "post_name, " \
    "post_modified, " \
    "post_modified_gmt, " \
    "guid, " \
    "post_type, " \
    "post_parent, " \
    "comment_count`" \
    ") VALUES (" \
    "1, " \
    "'{post_date}', " \
    "'{post_date_gmt}', " \
    "'{post_content}', " \
    "'{post_title}', '', '', '', '', " \
    "'publish', " \
    "'open', " \
    "'open', " \
    "'{post_name}', " \
    "'{post_modified}', " \
    "'{post_modified_gmt}', " \
    "'{guid}', " \
    "'{post_type}', " \
    "{post_parent} ,0);"


for chapter in range(1, 175):
    full_chapter = ""
    driver.get(url.format(chapter))
    with open('chapter_{}.txt'.format(chapter), 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    break
    element = driver.find_element(By.CLASS_NAME, "jsChapterWrapper")
    full_chapter = full_chapter + str(element.text) + "\n\n"
    print("Downloaded part 1 or chapter {}".format(chapter))
    part = re.findall(r"\(1/(\d)\)", str(element.text))
    if len(part) == 1:
        total_part = int(part[0])
        for p in range(2, total_part + 1):
            driver.get(url.format("{}_{}".format(chapter, p)))
            element = driver.find_element(By.CLASS_NAME, "jsChapterWrapper")
            full_chapter = full_chapter + str(element.text) + "\n\n"
            print("Downloaded part {} or chapter {}".format(p, chapter))
    with open('chapter_{}.txt'.format(chapter), 'w', encoding='utf-8') as f:
        f.write(full_chapter)
driver.close()
