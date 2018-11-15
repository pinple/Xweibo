header = {'Host': 'm.weibo.cn',
          'Connection': 'keep-alive',
          'Content-Length': 30,
          'Accept': 'application/json, text/plain, */*',
          'MWeibo-Pwa': 1,
          'X-Requested-With': 'XMLHttpRequest',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
          'Origin': 'https://m.weibo.cn',
          'Content-Type': 'application/x-www-form-urlencoded',
        #   'Referer': ' https://m.weibo.cn/profile/5610949777',
          'Accept-Encoding': 'gzip, deflate, br',
          'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
          'Cookie': ''
          }
WEIBO_USERNAME = os.environ.get('WEIBO_USERNAME')
WEIBO_PASSWORD = os.environ.get('WEIBO_PASSWORD')