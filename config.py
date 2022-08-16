PATH_TO_LIST_TRUYEN = 'truyenfull_list.json'
PATH_TO_TRUYEN_DES = 'truyen_description.json'
PATH_TO_CHAPTER_FOLDER = 'truyenfull'
PATH_TO_CATEGORIES_LIST = 'category_id_list.json'

HOST_PATH = "http://192.168.1.60/truyenraw-wordpress"

AUTH = ('admin', 'Thuong@1212')

INSERT_POST_API = "{}/wp-json/wp/v2/posts".format(HOST_PATH)
INSERT_CHAP_API = "{}/wp-json/wp/v2/chap".format(HOST_PATH)
INSERT_CATEGORY_API = "{}/wp-json/wp/v2/categories".format(HOST_PATH)
INSERT_AUTHOR_API = "{}/wp-json/wp/v2/tac-gia".format(HOST_PATH)
INSERT_SOURCE_API = "{}/wp-json/wp/v2/nguon".format(HOST_PATH)