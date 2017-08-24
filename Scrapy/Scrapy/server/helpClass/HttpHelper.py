import requests


class httpHelper(object):

    @staticmethod
    def httpGet(url,session,pageencoding=None,headers=None):
        try:

            if headers != None:
                 page = session.get(url,headers=headers)
            else:
                 page = session.get(url)

            if pageencoding != None:
                page.encoding = pageencoding
                return page.text

        except urllib2.URLError, e:
             if hasattr(e,"code"):
                print e.code
             if hasattr(e,"reason"):
                print e.reason

    @staticmethod
    def httPost(url,data,session,pageencoding=None,headers=None):
        try:

            if headers != None:
                 page = session.post(url,data=data,headers=headers)
            else:
                 page = session.post(url,data=data)

            if pageencoding != None:
                page.encoding = pageencoding
                return page.text

        except urllib2.URLError, e:
             if hasattr(e,"code"):
                print e.code
             if hasattr(e,"reason"):
                print e.reason