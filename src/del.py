import logging
import os
import json
import time

from config import WEIBO_PASSWORD, WEIBO_USERNAME
from weibo import WeiBo



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")
    weibo = WeiBo()
    weibo.login(WEIBO_USERNAME, WEIBO_PASSWORD)
    weibo.del_mblog()
