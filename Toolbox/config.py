PATH_TO_LIST_TRUYEN = 'truyenfull_list.json'
PATH_TO_TRUYEN_DES = 'truyen_description.json'
PATH_TO_CHAPTER_FOLDER = 'truyenfull'
PATH_TO_TAXONOMY_LIST = '{}_id_list.json'


AUTHOR = "tac-gia"
SOURCE = "nguon"
CATEGORY = "categories"

HOST_PATH = "https://truyenraw.net"

# HOST_PATH = "http://truyenraw.net"

AUTH = ('admin', 'Thuong@1212')

INSERT_POST_API = "{}/wp-json/wp/v2/posts".format(HOST_PATH)
INSERT_CHAP_API = "{}/wp-json/wp/v2/chap".format(HOST_PATH)
TAXONOMY_API = "{}/wp-json/wp/v2/{}"
UPLOAD_MEDIA_API = "{}/wp-json/wp/v2/media".format(HOST_PATH)
