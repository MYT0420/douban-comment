# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

class comment:
    def __init__(self, Url):
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.URL = Url
    def get_comment_Num(self):
        try:
            request = urllib2.Request(self.URL, headers=self.headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            pattern = re.compile('<div class="paginator"', re.S)
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接失败，错误原因", e.reason
                return None
    def get_movie_comment(self):
        try:
            request = urllib2.Request(self.URL, headers = self.headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            pattern = re.compile('<div xmlns:v=.*?typeof="v:Review".*?<span class=.*?title="(.*?)"></span>.*?<div class="main-bd">.*?<div class="short-content">(.*?)<a class=.*?</a>', re.S)
            items = re.findall(pattern, content)
            for item in items:
                print item[0], item[1]
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接失败，错误原因", e.reason
                return None
Url = 'http://movie.douban.com/review/best'
C = comment(Url)
C.get_movie_comment()
# __author__ = 'MYT'
