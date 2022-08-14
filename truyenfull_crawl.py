import requests
import re
import json

url_page = "https://truyenfull.vn/danh-sach/truyen-full/trang-{}/"
re_page = r"div class=\"row\" itemscope.+?data-desk-image=\"(.+?)\".+?a href=\"(.+?)\".+?>(.+?)<.+?author.+?</span>(.+?)</span>"

idx = 1

data_file = 'truyen_info_{}.json'
truyen_list = {}

if __name__ == "__main__":
    # for page in range(1, 633):
    #     page_html = requests.get(url_page.format(page))
    #     truyen_info = re.findall(re_page, page_html.text, re.DOTALL)
    #     for truyen in truyen_info:
    #         truyen_data = {
    #             "id": idx,
    #             "cover_url": truyen[0],
    #             "url": truyen[1],
    #             "name": truyen[2],
    #             "author": truyen[3]
    #         }
    #         truyen_list[idx] = truyen_data
    #         idx = idx + 1
    #     with open(data_file.format(page), 'a') as f:
    #         json.dump(truyen_list, f, indent=4, ensure_ascii=False)
    #     print("finish page {}".format(page))


    # get truyen introduce, category
    descripion_re = r"itemprop=\"description\">(.+?)</div>"
    category_re = r"(class=\"info\".+Thể loại:.+?title.+?>.+?<\/div>)"
    with open("truyenfull_list.json", 'r') as f:
        list_truyen = json.load(f)
        for id, data in list_truyen.items():
            page_html = requests.get(data['url'])
            des = re.findall(descripion_re, page_html.text, re.DOTALL)
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
                "source": source[0] if len(source) == 1 else ""
            }
            truyen_list[id] = truyen_data
            if int(id) % 100 == 0:
                with open("truyen_description.json".format(id), 'a') as f:
                     json.dump(truyen_list, f, indent=4, ensure_ascii=False)
                print("finish {} truyen".format(id))
                truyen_list = {}
