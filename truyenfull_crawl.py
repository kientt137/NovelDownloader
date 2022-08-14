import requests
import re
import json

url_page = "https://truyenfull.vn/danh-sach/truyen-full/trang-{}/"
re_page = r"div class=\"row\" itemscope.+?data-desk-image=\"(.+?)\".+?a href=\"(.+?)\".+?>(.+?)<.+?author.+?</span>(.+?)</span>"

idx = 1

data_file = 'truyen_info_{}.json'
truyen_list = {}

if __name__ == "__main__":
    for page in range(1, 633):
        page_html = requests.get(url_page.format(page))
        truyen_info = re.findall(re_page, page_html.text, re.DOTALL)
        for truyen in truyen_info:
            truyen_data = {
                "id": idx,
                "cover_url": truyen[0],
                "url": truyen[1],
                "name": truyen[2],
                "author": truyen[3]
            }
            truyen_list[idx] = truyen_data
            idx = idx + 1
        with open(data_file.format(page), 'a') as f:
            json.dump(truyen_list, f, indent=4, ensure_ascii=False)
        print("finish page {}".format(page))

    # with open("sample.html", "r", encoding='utf8') as file:
    #     content = file.read()
    #     truyen_info = re.findall(re_page, content, re.DOTALL)
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
    #     with open(data_file.format(), 'a') as f:
    #         json.dump(truyen_list, f, indent=4)
