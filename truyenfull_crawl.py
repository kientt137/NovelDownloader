import requests
import re
import json
from Toolbox.Utilities import Utilities as Utils
from Toolbox.config import *

url_page = "https://truyenfull.vn/danh-sach/truyen-full/trang-{}/"
re_page = r"div class=\"row\" itemscope.+?data-desk-image=\"(.+?)\".+?a href=\"(.+?)\".+?>(.+?)<.+?author.+?</span>(.+?)</span>"

idx = 1

data_file = 'truyen_info_{}.json'
truyen_list = {}

if __name__ == "__main__":
    descripion_re = r"itemprop=\"description\">(.+?)</div>"
    category_re = r"(class=\"info\".+Thể loại:.+?title.+?>.+?<\/div>)"
    cover_re = r"Thông tin truyện.+?img src=\"(.+?)\""

    list_truyen = Utils.load_json(PATH_TO_LIST_TRUYEN)
    for id, data in list_truyen.items():
        if int(id) < 11000:
            continue
        page_html = requests.get(data['url'])
        des = re.findall(descripion_re, page_html.text, re.DOTALL)
        cover_link = re.findall(cover_re, page_html.text, re.DOTALL)
        if len(des) == 0:
            print("truyen {} khong co description".format(id))
        category_html = re.findall(category_re, page_html.text, re.DOTALL)
        list_category = []
        if len(category_html) == 1:
            list_category = re.findall(r"itemprop=\"genre\".+?title=.+?>(.+?)<", category_html[0], re.DOTALL)
        else:
            print("truyen {} khong co category".format(id))
        source = re.findall(r"<span class=\"source\">(.+?)<", page_html.text)
        if len(source) == 0:
            print("truyen {} khong co source".format(id))
        truyen_data = {
            "id": id,
            "description": des[0] if len(des) == 1 else "",
            "category": list_category,
            "cover": cover_link[0] if len(cover_link) == 1 else "",
            "source": source[0] if len(source) == 1 else ""
        }
        truyen_list[id] = truyen_data
        if int(id) % 100 == 0:
            with open("truyen_description.json", 'a', encoding='utf8') as f:
                 json.dump(truyen_list, f, indent=4, ensure_ascii=False)
            print("finish {} truyen".format(id))
            truyen_list = {}
