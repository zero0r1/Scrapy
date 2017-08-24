class httpBase(object):
    def __init__(self):
        self.headers = {'accept': '*/*'
            ,'accept-encoding': 'gzip, deflate, sdch'
            ,'accept-language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2,ja;q=0.2'
            ,'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}

    def defaultHeaders(self):
        return self.headers

if __name__ == '__main__':
    httpBase()