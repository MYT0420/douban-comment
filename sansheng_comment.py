# -*- coding:utf-8 -*-
import urllib
import urllib2
from bs4 import BeautifulSoup
import re

def saveFile(data, i):
    path = "D:\\python-pro\\douban-comment\\paper_"+str(i+1)+".txt"
    file = open(path,'wb')
    page = 'page:'+str(i+1) +'\n'
    file.write(page.encode('gbk'))
    for d in data:
        d = str(d)+'\n'
        file.write(d.encode('gbk'))
    file.close()

class CrawlComment:
    def __init__(self, pageIdx=0, Url='http://movie.douban.com/subject/25823277/reviews?start='):
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.pageIdx = pageIdx
        self.URL = Url[0:Url.rfind('=') + 1] + str(pageIdx * 20)

    def setPage(self, index):
        self.URL = self.URL[0:self.URL.rfind('=') + 1] + str(idx)

    def get_title(self):
        pageCode = self.get_page()
        try:
            '''
            pattern = re.compile('<head>.*?<title>(.*?)</title>', re.S)
            items = re.findall(pattern, pageCode)
            return items
            '''
            soup = BeautifulSoup(pageCode, 'lxml')
            tag = soup.find('head', 'title')
            title = tag.title.get_text()
            return title
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接失败，错误原因", e.reason
                return None
    def get_comment_Num(self):
        pageCode = self.get_page()
        try:
            '''
            pattern = re.compile('<div class="paginator">.*?<span class="thispage" data-total-page="(.*?)">', re.S)
            items = re.findall(pattern, pageCode)[0]
            return items
            '''
            soup = BeautifulSoup(pageCode, 'html5lib')
            tag = soup.find('div',"paginator", 'data-total-page')
            total_page = tag.span.get_text()[0]
            return total_page
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接失败，错误原因", e.reason
                return None
    def get_comment(self):
        pageCode = self.get_page()
        ret = []
        try:
            #print pageCode
            '''
            pattern = re.compile('<div xmlns:v=.*?typeof="v:Review".*?<span property="v:rating".*?title="(.*?)"></span>.*?<div class="main-bd">.*?<div class="short-content">(.*?)<a.*?</a>', re.S)
            items = re.findall(pattern, pageCode)
            for item in items:
                ret.append('评分：' + item[0] + '\n' + '评价：' + item[1] + '\n')
            return ret
            '''
            soup = BeautifulSoup(pageCode, 'lxml')
            items = soup.find_all('div xmlns:v=', "v:Review", 'property', "short-content")
            for item in items:
                CS = item.title.get_text()
                C = item.short-content.get_text()
                ret.append('评分：' + item[0] + '\n' + '评价：' + item[1] + '\n')
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
spider = CrawlComment()
Num = int(spider.get_comment_Num())
print Num
for index in range(Num):
    spider.setPage(index)
    print 'index:'+ index
    comment = spider.get_comment()
    saveFile(comment, index)