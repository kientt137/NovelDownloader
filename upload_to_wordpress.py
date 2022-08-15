import re
import sys
import os.path
import json
import requests
import random
from config import *
from Utilities import Utilities as Utils


if __name__ == '__main__':
    id_from = int(sys.argv[1])
    id_to = int(sys.argv[2])
    if not os.path.exists(PATH_TO_CATEGORIES_LIST):
        print("Category file data not exist")
        exit()
    with open(PATH_TO_LIST_TRUYEN, 'r', encoding='utf8') as f1:
        list_truyen = json.load(f1)
        with open(PATH_TO_TRUYEN_DES, 'r', encoding='utf8') as f2:
            list_des = json.load(f2)
            with open(PATH_TO_CATEGORIES_LIST, 'r', encoding='utf8') as f3:
                list_category = json.load(f3)
                for i in range(id_from, id_to):
                    if os.path.exists("{}/truyenfull_{}.json".format(PATH_TO_CHAPTER_FOLDER, i)):
                        slug_info = re.findall(r"truyenfull.vn/(.+?)/", list_truyen[str(i)]['url'])
                        if len(slug_info) != 1:
                            slug = Utils.name2slug(list_truyen[str(i)]['name'])
                        else:
                            slug = slug_info[0]
                        categories = list_des[str(i)]['category']
                        categories_id = []
                        for cat in categories:
                            categories_id.append(str(list_category[Utils.name2slug(cat)]))
                        truyen_post = {
                            "slug": slug + "_" + str(random.randint(1000000, 9999999)),
                            "status": "publish",
                            "title": list_truyen[str(i)]['name'],
                            "content": list_des[str(i)]['description'],
                            "author": 1,
                            "excerpt": "",
                            "categories": ",".join(categories_id),
                            "terms": {
                                'nguon': 'suu-tamm'
                            }
                        }
                        res = requests.post(INSERT_POST_API, data=truyen_post, auth=AUTH)
                        if res.status_code == 201:
                            res_json = res.json()
                            id_post = res_json['id']
                            print("id_post = " + str(id_post))