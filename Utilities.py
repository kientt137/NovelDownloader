from unidecode import unidecode
import re


class Utilities:
    @staticmethod
    def name2slug(name):
        no_accent = unidecode(name)
        no_accent = re.sub(r"\s+", "_", no_accent.strip(), count=0, flags=0)
        print(no_accent)
        return no_accent.lower()
