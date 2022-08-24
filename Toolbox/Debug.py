import time


class Debug:
    @staticmethod
    def log(content):
        print("{}: {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), content))
