# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

class CrawlComment:
    def __init__(self, Url):
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.URL = Url
    def get_title(self):
        pageCode = self.get_page()
        try:
            pattern = re.compile('<head>.*?<title>(.*?)</title>', re.S)
            items = re.findall(pattern, pageCode)
            return items
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接失败，错误原因", e.reason
                return None
    def get_comment_Num(self):
        pageCode = self.get_page()
        try:
            pattern = re.compile('<div class="paginator">.*?<span class="thispage" data-total-page="(.*?)">', re.S)
            items = re.findall(pattern, pageCode)
            if items:
                return items
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接失败，错误原因", e.reason
                return None
    def get_comment(self):
        pageCode = self.get_page()
        try:
            #print pageCode
            pattern = re.compile('<div xmlns:v=.*?typeof="v:Review".*?<span property="v:rating".*?title="(.*?)"></span>.*?<div class="main-bd">.*?<div class="short-content">(.*?)<a.*?</a>', re.S)
            items = re.findall(pattern, pageCode)
            for item in items:
                print item[0], item[1]
            return items
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接失败，错误原因", e.reason
                return None
    def get_page(self):
        try:
            request = urllib2.Request(self.URL, headers = self.headers)
            response = urllib2.urlopen(request)
            page = response.read().decode('utf-8')
            #print page
            return page
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接失败，错误原因", e.reason
                return None

index = 0
baseUrl = 'http://movie.douban.com/subject/25823277/reviews?start='
url = baseUrl + 'index'
spider = CrawlComment(url)
Num = spider.get_comment_Num()
url_list = []
for i in range(int(Num[0])):
    url = baseUrl + str(i * 20)
    url_list.append(url)
    # print url_list
for j in url_list:
    CC = CrawlComment(j)
    T = CC.get_title()
    for k in T:
        print k
    CO = CC.get_comment()
    for q in CO:
        print q[0], q[1]