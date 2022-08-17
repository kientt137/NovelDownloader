import mariadb
import sys
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
import re
import os

url = "https://m.yushubo.cc/read_83404_{}.html"


# setup webdriver
op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(options=op, executable_path='Toolbox/chromedriver.exe')


# Connect to MariaDB Platform

def format_content(element):
    driver.execute_script("""
        var element = document.querySelector('h3');
        if (element)
            element.parentNode.removeChild(element);
        """, element)
    driver.execute_script("""
    var element = document.querySelector(".text-info");
    if (element)
        element.parentNode.removeChild(element);
    """, element)
    driver.execute_script("""
        var element = document.querySelector(".member");
        if (element)
            element.parentNode.removeChild(element);
        """, element)
    return element.text


for chapter in range(1, 175):
    full_chapter = ""
    driver.get(url.format(chapter))
    element = driver.find_element(By.CLASS_NAME, "jsChapterWrapper")
    chap_title = re.findall(r"第\d+章\s+?(.+?)\(", str(element.text))
    part = re.findall(r"\(1/(\d)\)", str(element.text))
    full_chapter = full_chapter + format_content(element) + "\n\n"
    print("Downloaded part 1 or chapter {}".format(chapter))
    if len(part) == 1:
        total_part = int(part[0])
        for p in range(2, total_part + 1):
            driver.get(url.format("{}_{}".format(chapter, p)))
            element = driver.find_element(By.CLASS_NAME, "jsChapterWrapper")
            full_chapter = full_chapter + format_content(element) + "\n\n"
            print("Downloaded part {} or chapter {}".format(p, chapter))
    with open('chapter_{}.txt'.format(chapter), 'w', encoding='utf-8') as f:
        f.write(full_chapter)
    if len(chap_title) != 0:
        os.rename('chapter_{}.txt'.format(chapter), 'chapter_{}_{}.txt'.format(chapter, chap_title[0]))
driver.close()
