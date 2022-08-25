import time

import requests
from unidecode import unidecode
from Toolbox.config import *
from Toolbox.Debug import Debug
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
    def get_taxonomy_id(list_taxonomy, type=CATEGORY):
        if not os.path.exists(PATH_TO_TAXONOMY_LIST.format(type)):
            taxonomy_list = {}
            res = Utilities.get_fetch(TAXONOMY_API.format(HOST_PATH, type))
            data_json = res.json()
            if len(data_json) > 0:
                for data in data_json:
                    taxonomy_list[data['slug']] = data['id']
            number_of_page = res.headers['X-WP-TotalPages']
            Debug.log("Taxonomy type {} has total {} records and split to {} pages"
                      .format(type, res.headers['X-WP-Total'], number_of_page))
            for i in range(2, int(number_of_page) + 1):
                res = Utilities.get_fetch(TAXONOMY_API.format(HOST_PATH, type) + "?page={}".format(i))
                data_json = res.json()
                if len(data_json) > 0:
                    for data in data_json:
                        taxonomy_list[data['slug']] = data['id']
            Utilities.dump_json(PATH_TO_TAXONOMY_LIST.format(type), taxonomy_list)
        result = []
        for taxonomy in list_taxonomy:
            name_slug = Utilities.name2slug(taxonomy)
            taxonomy_list = Utilities.load_json(PATH_TO_TAXONOMY_LIST.format(type))
            if name_slug in taxonomy_list:
                result.append(str(taxonomy_list[name_slug]))
            else:
                new_data = {
                    "name": taxonomy,
                    "slug": name_slug
                }
                res = Utilities.post_fetch(TAXONOMY_API.format(HOST_PATH, type), new_data,)
                if res.status_code == 201:
                    id = res.json()['id']
                    Debug.log("Inserted new {}: {}".format(type, taxonomy))
                    taxonomy_list[name_slug] = id
                    Utilities.dump_json(PATH_TO_TAXONOMY_LIST.format(type), taxonomy_list)
                    result.append(str(id))
        return ','.join(result)

    @staticmethod
    def load_json(path):
        try:
            with open(path, 'r', encoding='utf8') as f:
                return json.load(f)
        except Exception as e:
            Debug.log("Load json from " + path + ": something has wrong")
            Debug.log(str(e))
            exit()

    @staticmethod
    def dump_json(path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def dump_json_a(path, data):
        with open(path, 'a') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def post_fetch(url, data, try_again=True):
        while True:
            Debug.log("Request POST {}".format(url))
            try:
                res = requests.post(url, json=data, auth=AUTH)
                if res.status_code == 201:
                    return res
                else:
                    Debug.log("Error {} with POST request {}. Try again after 5 seconds".format(res.status_code, url))
            except requests.RequestException as e:
                Debug.log(str(e))
                Debug.log("Try again after 5 seconds")
            time.sleep(5)

    @staticmethod
    def get_fetch(url, try_again=True):
        while True:
            Debug.log("Request GET {}".format(url))
            try:
                res = requests.get(url, auth=AUTH)
                if res.status_code == 200:
                    return res
                else:
                    Debug.log("Error {} with GET request {}. Try again after 5 seconds".format(res.status_code, url))
            except requests.RequestException as e:
                Debug.log(str(e))
                Debug.log("Try again after 5 seconds")
            time.sleep(5)
