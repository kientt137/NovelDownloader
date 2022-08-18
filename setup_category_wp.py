import json
import requests
from Toolbox.Utilities import Utilities as Utils
from Toolbox.config import *

# set_category = []

# with open(PATH_TO_TRUYEN_DES, 'r', encoding='utf8') as f2:
#     list_des = json.load(f2)
#     for id, data in list_des.items():
#         for category in data['category']:
#             if category not in set_category:
#                 set_category.append(category)
# print(set_category)

set_category = ['Bách Hợp', 'Cung Đấu', 'Cổ Đại', 'Dị Giới', 'Dị Năng', 'Đam Mỹ', 'Điền Văn', 'Đoản Văn', 'Đô Thị',
                'Đông Phương', 'Gia Đấu', 'Huyền Huyễn', 'Hài Hước', 'Hệ Thống', 'Khoa Huyễn', 'Khác', 'Kiếm Hiệp',
                'Light Novel', 'Linh Dị', 'Lịch Sử', 'Mạt Thế', 'Ngôn Tình', 'Ngược', 'Nữ Cường', 'Nữ Phụ',
                'Phương Tây', 'Quan Trường', 'Quân Sự', 'Sắc', 'Sủng', 'Thám Hiểm', 'Tiên Hiệp', 'Trinh Thám',
                'Truyện Teen', 'Trọng Sinh', 'Việt Nam', 'Võng Du', 'Xuyên Không', 'Xuyên Nhanh']

categories_id = {}
for category in set_category:
    slug = Utils.name2slug(category)
    category_data = {
        "name": category,
        "slug": slug
    }
    response = requests.post(TAXONOMY_API.format(HOST_PATH, CATEGORY), json=category_data, auth=AUTH)
    if response.status_code == 201:
        print("Add category " + category + " successfully")
        categories_id[slug] = response.json()['id']

with open("categories_id_list.json".format(id), 'a') as f:
    json.dump(categories_id, f, indent=4, ensure_ascii=False)
