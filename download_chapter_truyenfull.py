import json
import requests
import re
import sys

chapter_url = "{}chuong-{}"

chap_content_re = r"itemprop=\"articleBody\".+?<div.+?ads-responsive.+?/div>(.+?)</div"
chap_title_re = r"<span class=\"chapter-text\">(.+?)</a>"

if __name__ == "__main__":
    id_from = int(sys.argv[1])
    id_to = int(sys.argv[2])

    with open("truyenfull_list.json", 'r') as f:
        list_truyen = json.load(f)
        for id, data in list_truyen.items():
            if id_from <= int(id) < id_to:
                truyen_data = {}
                chap_num = 1
                while True:
                    chapter_url_full = chapter_url.format(data['url'], chap_num)
                    page_html = requests.get(chapter_url_full)
                    if "Thông tin truyện" in page_html.text:
                        if len(truyen_data) != 0:
                            with open("truyenfull/truyenfull_{}.json".format(id), 'a') as f:
                                json.dump(truyen_data, f, indent=4, ensure_ascii=False)
                            print("Truyen {} finish, has {} chapter".format(id, chap_num))
                        else:
                            print("Truyen {} finish, has 0 chapter".format(id))
                        break
                    chap_content = re.findall(chap_content_re, page_html.text, re.DOTALL)
                    if len(chap_content) != 1:
                        print("chap {} of {} do not have content".format(chap_num, id))
                        break
                    chap_title = re.findall(chap_title_re, page_html.text, re.DOTALL)
                    if len(chap_title) != 1:
                        print("chap {} of {} do not have title".format(chap_num, id))
                        break
                    else:
                        title = chap_title[0].strip().replace("<span>", "").replace("</span>", "")
                    chapter_data = {
                        "chapter": chap_num,
                        "title": title,
                        "content": chap_content[0]
                    }
                    print("Download success chapter {} of {}".format(chap_num, data['name']))
                    truyen_data[chap_num] = chapter_data
                    chap_num = chap_num + 1
