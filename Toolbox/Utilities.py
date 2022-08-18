import requests
from unidecode import unidecode
from Toolbox.config import *
import os.path
import json
import re


class Utilities:
    @staticmethod
    def name2slug(name):
        no_accent = unidecode(name)
        regex = re.compile('[^a-zA-Z\d\s]')
        slug = regex.sub('', no_accent)
        slug = re.sub(r"\s+", "_", slug.strip(), count=0, flags=0)
        return slug.lower()

    @staticmethod
    def upload_cover_image(path):
        mediaImageBytes = open(path, 'rb').read()

        uploadImageFilename = "661b943654f54bd4b2711264eb275e1b.jpg"
        curHeaders = {
            "Content-Type": "image/jpeg",
            "Accept": "application/json",
            'Content-Disposition': "attachment; filename=%s" % uploadImageFilename,
        }

        resp = requests.post(UPLOAD_MEDIA_API, headers=curHeaders, data=mediaImageBytes, auth=AUTH)
        return {
            "status_code": resp.status_code,
            "media_id": resp.json()['id'] if resp.status_code == 201 else ''
        }

    @staticmethod
    def download_image_from_url(url, file_name):
        img_data = requests.get(url).content
        with open(file_name, 'wb') as handler:
            handler.write(img_data)

    @staticmethod
    def get_taxonomy_id(name, type=CATEGORY):
        if not os.path.exists(PATH_TO_TAXONOMY_LIST.format(type)):
            taxonomy_list = {}
            res = requests.get(TAXONOMY_API.format(HOST_PATH, type), auth=AUTH)
            data_json = res.json()
            if len(data_json) > 0:
                for data in data_json:
                    taxonomy_list[data['slug']] = data['id']
            Utilities.dump_json(PATH_TO_TAXONOMY_LIST.format(type), taxonomy_list)
        name_slug = Utilities.name2slug(name)
        taxonomy_list = Utilities.load_json(PATH_TO_TAXONOMY_LIST.format(type))
        if name_slug in taxonomy_list:
            return str(taxonomy_list[name_slug])
        else:
            new_data = {
                "name": name,
                "slug": name_slug
            }
            res = requests.post(TAXONOMY_API.format(HOST_PATH, type), json=new_data, auth=AUTH)
            if res.status_code == 201:
                id = res.json()['id']
                print("Inserted new {}: {}".format(type, name))
                taxonomy_list[name_slug] = id
                Utilities.dump_json(PATH_TO_TAXONOMY_LIST.format(type), taxonomy_list)
                return id

    @staticmethod
    def load_json(path):
        try:
            with open(path, 'r', encoding='utf8') as f:
                return json.load(f)
        except Exception as e:
            print("Load json from " + path + ": something has wrong")
            print(str(e))
            exit()

    @staticmethod
    def dump_json(path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
