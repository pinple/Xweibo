import logging
import os

from weibo import WeiBo
from config import WEIBO_USERNAME, WEIBO_PASSWORD

weibo = WeiBo()
weibo.login(WEIBO_USERNAME, WEIBO_PASSWORD)


def del_myblog(mid):
    url = 'http://weibo.com/aj/mblog/del?ajwvr=6'
    data = {'mid': mid}
    response = weibo.post(url, data)
    logging.debug('del status: %s', response.status_code)
    print(response.status_code)
    print(response.content)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")
    del_myblog('')
