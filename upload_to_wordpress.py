import re
import sys
import os.path
import json
import requests
import random
from Toolbox.config import *
from Toolbox.Utilities import Utilities as Utils


if __name__ == '__main__':
    id_from = int(sys.argv[1])
    id_to = int(sys.argv[2])
    if not os.path.exists(PATH_TO_TAXONOMY_LIST.format(CATEGORY)):
        print("Category file data not exist")
        exit()
    with open(PATH_TO_LIST_TRUYEN, 'r', encoding='utf8') as f1:
        list_truyen = json.load(f1)
        with open(PATH_TO_TRUYEN_DES, 'r', encoding='utf8') as f2:
            list_des = json.load(f2)
            with open(PATH_TO_TAXONOMY_LIST.format(CATEGORY), 'r', encoding='utf8') as f3:
                list_category = json.load(f3)
                for i in range(id_from, id_to):
                    if os.path.exists("{}/truyenfull_{}.json".format(PATH_TO_CHAPTER_FOLDER, i)):
                        # slug setup
                        slug_info = re.findall(r"truyenfull.vn/(.+?)/", list_truyen[str(i)]['url'])
                        if len(slug_info) != 1:
                            slug = Utils.name2slug(list_truyen[str(i)]['name'])
                        else:
                            slug = slug_info[0]
                        slug = slug + "_" + str(random.randint(1000000, 9999999))
                        # category setup
                        categories = list_des[str(i)]['category']
                        categories_id = []
                        for cat in categories:
                            categories_id.append(str(list_category[Utils.name2slug(cat)]))
                        # cover image setup
                        cover_path = "cover/{}.jpg".format(slug)
                        Utils.download_image_from_url(list_truyen[str(i)]['cover_url'], cover_path)
                        upload_res = Utils.upload_cover_image(cover_path)
                        media_id = upload_res["media_id"] if upload_res["status_code"] == 201 else 0
                        author_id = Utils.get_taxonomy_id(list_truyen[str(i)]['author'], AUTHOR)
                        source_id = Utils.get_taxonomy_id(list_des[str(i)]['source'], SOURCE)
                        truyen_post = {
                            "slug": slug,
                            "status": "publish",
                            "title": str(list_truyen[str(i)]['name']),
                            "content": str(list_des[str(i)]['description']),
                            "author": 1,
                            "excerpt": "",
                            "categories": ",".join(categories_id),
                            "meta": {
                                "tw_multi_chap": 1,
                                "tw_status": "Full",
                                "tw_loai": "Dịch"
                            },
                            "featured_media": int(media_id),
                            "tac-gia": str(author_id),
                            "nguon": str(source_id)
                        }
                        res = requests.post(INSERT_POST_API, json=truyen_post, auth=AUTH)
                        if res.status_code == 201:
                            res_json = res.json()
                            id_post = res_json['id']
                            with open("{}/truyenfull_{}.json".format(PATH_TO_CHAPTER_FOLDER, i), 'r', encoding='utf8') as f4:
                                list_chap = json.load(f4)
                                for chap, data in list_chap.items():
                                    slug = "chuong_" + str(data['chapter']) + "_" + str(random.randint(1000, 9999))
                                    chap_data = {
                                        "slug": slug,
                                        "status": "publish",
                                        "parent": id_post,
                                        "title": str(data['title']),
                                        "content": str(data['content']),
                                        "ping_status": "open"
                                    }
                                    res_chap = requests.post(INSERT_CHAP_API, json=chap_data, auth=AUTH)
                                    if res_chap.status_code == 201:
                                        print("Insert success chapter {}".format(chap))
                                print("Finish upload {}".format(list_truyen[str(i)]['name']))
