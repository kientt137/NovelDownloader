# from Toolbox.Utilities import Utilities as Utils
# from Toolbox.Debug import Debug
# from Toolbox.config import *
import requests
import re
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("/Users/kien-pc/PycharmProjects/NovelDownloader/Toolbox/truyenraw-64e91-firebase-adminsdk-9chfa-b94f0c803b.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://truyenraw-64e91-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
ref = db.reference('/yushubo')

url_crawl = 'https://m.yushubo.cc/histp/rank/order/hits.html'
base_url = "https://m.yushubo.cc{}"

# res = requests.get(url_crawl)
url_novel = ['/book_62635.html', '/book_49165.html', '/book_103170.html', '/book_134920.html', '/book_59491.html', '/book_36227.html', '/book_115574.html', '/book_145209.html', '/book_52801.html', '/book_95118.html', '/book_127630.html', '/book_93468.html', '/book_67189.html', '/book_40333.html', '/book_85919.html', '/book_117639.html', '/book_33916.html', '/book_34523.html', '/book_54435.html', '/book_136727.html', '/book_40374.html', '/book_91412.html', '/book_75478.html', '/book_36229.html', '/book_139900.html', '/book_137291.html', '/book_141273.html', '/book_110491.html', '/book_148852.html', '/book_54493.html']
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
            'source_url': base_url.format(url)
        })


