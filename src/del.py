import logging
import os
import json
import time

from config import WEIBO_PASSWORD, WEIBO_USERNAME
from weibo import WeiBo

weibo = WeiBo()
weibo.login(WEIBO_USERNAME, WEIBO_PASSWORD)


def del_mblog():
    url = 'http://weibo.com/aj/mblog/del?ajwvr=6'
    mids = weibo.get_mblog_mids()
    print('mids:{0}'.format(mids))
    for mid in mids:
        data = {'mid': mid}
        response = weibo.post(url, data=json.dumps(data))
        logging.debug('del status:', response.status_code)
        print('del status: ', response.status_code)
        print(response.content.decode('utf8'))
        time.sleep(2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")
    del_mblog()
