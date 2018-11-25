# _*_ coding: utf-8 _*_
import os
import re
import rsa
import time
import json
import base64
import logging
import binascii
import requests
import urllib.parse

from helper import parse_mblog_mids
from config import WEIBO_USERNAME, WEIBO_PASSWORD

class WeiBo(object):
    """
    class of WeiBo, to login weibo.com
    """

    def __init__(self):
        """
        constructor
        """
        self.user_name = None
        self.pass_word = None
        self.user_uniqueid = None
        self.user_nick = None

        self.session = requests.Session()
        self.session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"})
        self.session.get("http://weibo.com/login.php")
        return

    def login(self, user_name, pass_word):
        """
        login weibo.com, return True or False
        """
        self.user_name = user_name
        self.pass_word = pass_word
        self.user_uniqueid = None
        self.user_nick = None

        # get json data
        s_user_name = self.get_username()
        json_data = self.get_json_data(su_value=s_user_name)
        if not json_data:
            return False
        s_pass_word = self.get_password(json_data["servertime"], json_data["nonce"], json_data["pubkey"])

        # make post_data
        post_data = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "userticket": "1",
            "vsnf": "1",
            "service": "miniblog",
            "encoding": "UTF-8",
            "pwencode": "rsa2",
            "sr": "1280*800",
            "prelt": "529",
            "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "rsakv": json_data["rsakv"],
            "servertime": json_data["servertime"],
            "nonce": json_data["nonce"],
            "su": s_user_name,
            "sp": s_pass_word,
            "returntype": "TEXT",
        }

        # get captcha code
        if json_data["showpin"] == 1:
            url = "http://login.sina.com.cn/cgi/pin.php?r=%d&s=0&p=%s" % (int(time.time()), json_data["pcid"])
            with open("captcha.jpeg", "wb") as file_out:
                file_out.write(self.session.get(url).content)
            code = input("请输入验证码:")
            post_data["pcid"] = json_data["pcid"]
            post_data["door"] = code

        # login weibo.com
        login_url_1 = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=%d" % int(time.time())
        json_data_1 = self.session.post(login_url_1, data=post_data).json()
        if json_data_1["retcode"] == "0":
            params = {
                "callback": "sinaSSOController.callbackLoginStatus",
                "client": "ssologin.js(v1.4.18)",
                "ticket": json_data_1["ticket"],
                "ssosavestate": int(time.time()),
                "_": int(time.time()*1000),
            }
            response = self.session.get("https://passport.weibo.com/wbsso/login", params=params)
            json_data_2 = json.loads(re.search(r"\((?P<result>.*)\)", response.text).group("result"))
            if json_data_2["result"] is True:
                self.user_uniqueid = json_data_2["userinfo"]["uniqueid"]
                self.user_nick = json_data_2["userinfo"]["displayname"]
                logging.warning("WeiBo succeed: %s", json_data_2)
            else:
                logging.warning("WeiBo failed: %s", json_data_2)
        else:
            logging.warning("WeiBo failed: %s", json_data_1)
        return True if self.user_uniqueid and self.user_nick else False

    def get_username(self):
        """
        get legal username
        """
        username_quote = urllib.parse.quote_plus(self.user_name)
        username_base64 = base64.b64encode(username_quote.encode("utf-8"))
        return username_base64.decode("utf-8")

    def get_json_data(self, su_value):
        """
        get the value of "servertime", "nonce", "pubkey", "rsakv" and "showpin", etc
        """
        params = {
            "entry": "weibo",
            "callback": "sinaSSOController.preloginCallBack",
            "rsakt": "mod",
            "checkpin": "1",
            "client": "ssologin.js(v1.4.18)",
            "su": su_value,
            "_": int(time.time()*1000),
        }
        try:
            response = self.session.get("http://login.sina.com.cn/sso/prelogin.php", params=params)
            json_data = json.loads(re.search(r"\((?P<data>.*)\)", response.text).group("data"))
        except Exception as excep:
            json_data = {}
            logging.error("WeiBo get_json_data error: %s", excep)

        logging.debug("WeiBo get_json_data: %s", json_data)
        return json_data

    def get_password(self, servertime, nonce, pubkey):
        """
        get legal password
        """
        string = (str(servertime) + "\t" + str(nonce) + "\n" + str(self.pass_word)).encode("utf-8")
        public_key = rsa.PublicKey(int(pubkey, 16), int("10001", 16))
        password = rsa.encrypt(string, public_key)
        password = binascii.b2a_hex(password)
        return password.decode()

    def post(self, url, data, **kwargs):
        return self.session.post(url, data=data, **kwargs)

    def get_mblog_mids(self):
        url = 'https://weibo.com/p/aj/v6/mblog/mbloglist'
        params = {
                'ajwvr': '6',
                'domain':'100505',
                'is_search': '0',
                'visible': '0',
                'is_all': '1',
                'is_tag': '0',
                'profile_ftype': '1',
                'page': '1',
                'pagebar': '1',
                'pl_name':'Pl_Official_MyProfileFeed__19',
                'id': '100505' + self.user_uniqueid,
                'script_uri': '/' + self.user_uniqueid + '/profile',
                'feed_type': '0',
                'pre_page': '5',
                'domain_op': '100505',
                '__rnd': str(time.time()*1000)[:13]
        }
        response = self.session.get(url, params=params)
        ret = response.json()
        code = ret.get('code')
        data = ret.get('data')
        prog = re.compile('\s+mid="(\d+)"\s+')
        result = prog.findall(data)
        logging.info('mid list: {0}'.format(result))
        logging.info('length: {0}'.format(len(set(result))))
        return set(result)

    def del_mblog(self):
        url = 'https://weibo.com/aj/mblog/del?ajwvr=6'
        count = 1
        while True:
            mids = self.get_mblog_mids()
            if not mids:
                logging.info('这里似乎没有微博了，10秒后自动重试...')
                time.sleep(10)
            headers = {'Referer': 'http://weibo.com/{0}/profile?rightmod=1&wvr=6&mod=personnumber&is_all=1'.format(self.user_uniqueid)}
            for mid in mids:
                data = {'mid': mid}
                response = self.post(url, data=data, headers=headers)
                ret = response.json()
                ret_code = ret.get('code')
                if ret_code == '100000':
                    logging.info('成功删除第{0}条微博...'.format(str(count)))
                    count += 1
                    time.sleep(1)
                else:
                    logging.error('删除失败，请检查重试！')
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")
    weibo = WeiBo()
    weibo.login(WEIBO_USERNAME, WEIBO_PASSWORD)
