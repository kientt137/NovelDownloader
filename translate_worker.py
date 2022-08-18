import re
from os import listdir
from os.path import isfile, join
import requests
from unidecode import unidecode

onlyfiles = [f for f in listdir('truyen_raw/') if isfile(join('truyen_raw/', f))]
url = 'http://www.vietphrase.info/Vietphrase/TranslateVietPhraseS'

url_api = "http://localhost/truyenraw-wordpress/wp-json/wp/v2/chap"

dic_chapter_name = {}
dic_chapter_file = {}


def format_name(name):
    no_accent = unidecode(name)
    no_accent = re.sub(r"\s+", "_", no_accent.strip(), count=0, flags=0)
    print(no_accent)
    return no_accent.lower()


for file in onlyfiles:
    str = re.findall(r"chapter_(.+?)_(.+?).txt", file)
    dic_chapter_name[int(str[0][0])] = str[0][1]
    dic_chapter_file[int(str[0][0])] = file

for i in sorted(dic_chapter_name.keys()):
    myobj = {'chineseContent': dic_chapter_name[i]}
    chapter_name = requests.post(url, json=myobj)
    with open("truyen_raw/{}".format(dic_chapter_file[i]), encoding="utf8") as f:
        inp = f.read()
        myobj = {'chineseContent': inp}
        dich_full = requests.post(url, json=myobj)
        with open('truyen_raw/dich/chapter_{}_{}.txt'.format(i, format_name(chapter_name.text)), 'w', encoding='utf8') as f:
            f.write(dich_full.text)
        # print(x.text)

        post_chap_req = {
            "status": "publish",
            "title": "Chương {}: {}".format(i, chapter_name.text),
            "content": dich_full.text,
            "ping_status": "open",
            "slug": format_name(chapter_name.text),
            "parent": 6
        }
        upload = requests.post(url_api, json=post_chap_req, auth=('admin', 'Thuong@1212'))
