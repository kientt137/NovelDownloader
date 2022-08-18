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
    list_truyen = Utils.load_json(PATH_TO_LIST_TRUYEN)
    list_des = Utils.load_json(PATH_TO_TRUYEN_DES)
    for i in range(id_from, id_to):
        upload_result = {str(i): {}}
        try:
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
                if len(categories) == 0:
                    categories_id = Utils.get_taxonomy_id(['Đang cập nhật'], type=CATEGORY)
                else:
                    categories_id = Utils.get_taxonomy_id(list_des[str(i)]['category'], type=CATEGORY)
                # cover image setup
                # cover_path = "cover/{}.jpg".format(slug)
                # Utils.download_image_from_url(list_des[str(i)]['cover'], cover_path)

                random_img = ""
                while ".jpeg" not in random_img:
                    random_img = random.choice(os.listdir("random_image"))
                upload_res = Utils.upload_cover_image("random_image/{}".format(random_img))
                media_id = upload_res["media_id"] if upload_res["status_code"] == 201 else 0
                author = list_truyen[str(i)]['author'] if list_truyen[str(i)]['author'] != "" else "Đang cập nhật"
                author_id = Utils.get_taxonomy_id([author], AUTHOR)
                source = list_des[str(i)]['source'] if list_des[str(i)]['source'] != "" else "Sưu tầm"
                source_id = Utils.get_taxonomy_id([source], SOURCE)
                truyen_post = {
                    "slug": slug,
                    "status": "publish",
                    "title": str(list_truyen[str(i)]['name']),
                    "content": str(list_des[str(i)]['description']),
                    "author": 1,
                    "excerpt": "",
                    "categories": categories_id,
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
                    upload_result[str(i)]['post_id'] = str(id_post)
                    with open("{}/truyenfull_{}.json".format(PATH_TO_CHAPTER_FOLDER, i), 'r', encoding='utf8') as f4:
                        list_chap = json.load(f4)
                        upload_result[str(i)]['chapter'] = {}
                        for chap in range(1, len(list_chap) + 1):
                            slug = "chuong_" + str(list_chap[str(chap)]['chapter']) + "_" + str(random.randint(1000, 9999))
                            title = str(list_chap[str(chap)]['title'])
                            title = re.sub(r"<.+?>", "", title.strip(), count=0, flags=0)
                            chap_data = {
                                "slug": slug,
                                "status": "publish",
                                "parent": id_post,
                                "title": title,
                                "content": str(list_chap[str(chap)]['content']),
                                "ping_status": "open"
                            }
                            res_chap = requests.post(INSERT_CHAP_API, json=chap_data, auth=AUTH)
                            if res_chap.status_code == 201:
                                print("Insert success chapter {}".format(chap))
                                upload_result[str(i)]['chapter'][str(chap)] = res_chap.json()['id']
                        upload_result[str(i)]['status'] = "finish"
                        print("Finish upload {}".format(list_truyen[str(i)]['name']))
            else:
                print("File chapter data of novel id {} not exist".format(i))
        except Exception as e:
            print(str(e))
            upload_result[str(i)]['status'] = "error {}".format(str(e))
        Utils.dump_json_a("result_upload.json", upload_result)
