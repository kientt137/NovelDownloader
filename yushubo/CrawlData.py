from Toolbox.Utilities import Utilities as Utils
from Toolbox.Debug import Debug
from Toolbox.config import *
import re
import firebase_admin
from firebase_admin import credentials, db
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import os


cred = credentials.Certificate("F:\\PycharmProjects\\NovelDownloader\\Toolbox\\truyenraw-64e91-firebase-adminsdk-9chfa-b94f0c803b.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://truyenraw-64e91-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
ref = db.reference('/yushubo')

url_crawl = 'https://m.yushubo.cc/histp/rank/order/hits.html'
base_url = "https://m.yushubo.cc{}"


def update_firebase(book_id, current_chap, status):
    ref_book = ref.child('{}'.format(book_id))
    if ref_book.get() is not None:
        ref_book.update({
            'current_chap': current_chap,
            'status': status,
            'last_update': time.strftime("%Y-%m-%d %H:%M:%S")
        })


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


def get_chapter_content(chapter, url_chap):
    full_chapter = ""
    driver.get(url_chap.format(chapter))
    element = driver.find_element(By.CLASS_NAME, "jsChapterWrapper")
    chap_title = re.findall(r"第\d+章\s+?(.+?)\(", str(element.text))
    part = re.findall(r"\(1/(\d)\)", str(element.text))
    full_chapter = full_chapter + format_content(element) + "\n\n"
    print("Downloaded part 1 or chapter {}".format(chapter))
    if len(part) == 1:
        total_part = int(part[0])
        for p in range(2, total_part + 1):
            driver.get(url_chap.format("{}_{}".format(chapter, p)))
            element = driver.find_element(By.CLASS_NAME, "jsChapterWrapper")
            full_chapter = full_chapter + format_content(element) + "\n\n"
            print("Downloaded part {} or chapter {}".format(p, chapter))
    with open('chapter_{}.txt'.format(chapter), 'w', encoding='utf-8') as f:
        f.write(full_chapter)
    if len(chap_title) != 0:
        os.rename('chapter_{}.txt'.format(chapter), 'chapter_{}_{}.txt'.format(chapter, chap_title[0]))
    driver.close()


if __name__ == "__main__":
    # res = requests.get(url_crawl)
    url_novel = ['/book_62635.html', '/book_49165.html', '/book_103170.html', '/book_134920.html', '/book_59491.html',
                 '/book_36227.html', '/book_115574.html', '/book_145209.html', '/book_52801.html', '/book_95118.html',
                 '/book_127630.html', '/book_93468.html', '/book_67189.html', '/book_40333.html', '/book_85919.html',
                 '/book_117639.html', '/book_33916.html', '/book_34523.html', '/book_54435.html', '/book_136727.html',
                 '/book_40374.html', '/book_91412.html', '/book_75478.html', '/book_36229.html', '/book_139900.html',
                 '/book_137291.html', '/book_141273.html', '/book_110491.html', '/book_148852.html', '/book_54493.html']
    # if res.status_code == 200:
    #     html = res.text
    #     url_novel = re.findall(r"x-book x-rank_book van-hairline-bottom.+?href=\"(.+?)\"", html, re.DOTALL)
    #     print(url_novel)
    for url in url_novel:
        id_novel = re.findall(r"_(.+?)\.", url)
        id_novel = int(id_novel[0])
        ref_novel = ref.child('{}'.format(id_novel))
        if ref_novel.get() is None:
            ref_novel.set({
                'current_chap': 0,
                'truyenraw_id': 0,
                'status': 'ongoing',
                'source_url': base_url.format(url),
                'last_update': time.strftime("%Y-%m-%d %H:%M:%S")
            })
        full_url = base_url.format(url)
        html = Utils.get_fetch(full_url)

        meta_list = ['category', 'author', 'book_name', 'read_url', 'status', 'update_time']
        meta_data = {}
        pattern = r"meta property=\"og:novel:{}\" content=\"(.+?)\""
        for meta in meta_list:
            data = re.findall(pattern.format(meta), html.text)
            if len(data) != 1:
                print("meta {} in {} not found".format(meta, full_url))
            meta_data[meta] = data[0]
        pattern_book_info = re.findall(r"(class=\"book-info\".+?mod-head)", html.text, re.DOTALL)
        cover_url = re.findall(r"img class=\"lazy\" src=\"(.+?)\"", pattern_book_info[0], re.DOTALL)
        number_of_chaper = re.findall(r"总共.+?>(.+?)<", pattern_book_info[0], re.DOTALL)
        description = re.findall(r"<div class=\"content\">.+?<p>(.+?)</p>", pattern_book_info[0], re.DOTALL)
        print("{} {} {}".format(cover_url[0], number_of_chaper[0], description[0]))
        print(meta_data)

