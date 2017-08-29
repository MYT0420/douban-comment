#encoding:utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import csv
import socket
import cookielib
import urllib
import urllib2
import requests
from bs4 import BeautifulSoup
import re
import random
import time

def saveFile(data, i):
	filename = "./result/"+str(i+1)+".txt"
	fout = open(filename,'wb')
	page = 'page:'+str(i+1) +'\n'
	print >> fout,page
	for d in data:
		d = str(d)
		print >> fout,d
	fout.close()
def IPspider(numpage):
	csvfile = file('ips.csv', 'wb')    
	writer = csv.writer(csvfile)  
	url='http://www.xicidaili.com/nn/'  
	user_agent='IP'  
	headers={'User-agent':user_agent}  
	for num in xrange(1,numpage+1):  
		ipurl=url+str(num)  
		print 'Now downloading the '+str(num*100)+' ips'  
		request=urllib2.Request(ipurl,headers=headers)
		content=urllib2.urlopen(request).read()
		bs=BeautifulSoup(content,'html.parser') 
		#print bs
		res=bs.find_all('tr')
		for item in res:
			try:
				#print item
				temp = []
				tds = item.find_all('td')
				if len(tds) == 0 :
					continue
				#print tds
				#raw_input('---')
				temp.append(tds[1].text.encode('utf-8')+':'+tds[2].text.encode('utf-8'))
				#print 'temp:',temp
				writer.writerow(temp)
			except IndexError:
				pass
def IPpool():
	socket.setdefaulttimeout(2)
	reader=csv.reader(open('ips.csv'))
	IPpool=[]
	for row in reader:
		#print row
		#raw_input('---')
		proxy=row[0]
		proxy_handler=urllib2.ProxyHandler({"http":proxy})
		opener=urllib2.build_opener(proxy_handler)
		urllib2.install_opener(opener)
		try:
			html=urllib2.urlopen('https://movie.douban.com')
			IPpool.append(row[0])
		except Exception,e:
			continue
	print IPpool
	return IPpool

class CrawlComment:
	def __init__(self, pageIdx=0, Url='http://movie.douban.com/subject/25823277/reviews?start='):
		self.user_agents = [
		#'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
		#'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:46.0) Gecko/20100101 Firefox/46.0',
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:46.0) Gecko/20100101 Firefox/46.0',
		#'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
		#'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8'
		]
		#IPspider(1)
		self.ippool = IPpool()
		#self.cookie = self.get_cookie()
		#self.headers = {'User-Agent': self.user_agent, 'cookie': self.cookie}
		self.pageIdx = pageIdx
		self.URL = Url[0:Url.rfind('=') + 1] + str(pageIdx * 20)
		self.run_time = 0
		
	def setPage(self, index):
		self.URL = self.URL[0:self.URL.rfind('=') + 1] + str(index)

	def get_title(self):
		pageCode = self.get_page()
		total_time = 200
		while pageCode == None and total_time > 0:
			pageCode = self.get_page()
			total_time -= 1
		try:
			'''
			pattern = re.compile('<head>.*?<title>(.*?)</title>', re.S)
			items = re.findall(pattern, pageCode)
			return items
			'''
			soup = BeautifulSoup(pageCode, 'lxml')
			tag = soup.find('div', attrs={'id':'content'})
			title = tag.h1.get_text()
			#print title
			return title
		except urllib2.URLError as e:
			if hasattr(e, "reason"):
				print u"连接失败，错误原因", e.reason
				return None
	
	def get_comment_Num(self):
		total_time = 200
		pageCode = self.get_page()
		while pageCode == None and total_time > 0:
			total_time -= 1
			pageCode = self.get_page()
		try:
			'''
			pattern = re.compile('<div class="paginator">.*?<span class="thispage" data-total-page="(.*?)">', re.S)
			items = re.findall(pattern, pageCode)[0]
			return items
			'''
			soup = BeautifulSoup(pageCode, 'lxml')
			#print soup
			tag = soup.findAll('span', attrs={'class':'thispage'})
			#print tag
			if len(tag) == 0:
				raw_input('--')
				print soup
			total_page = int(tag[0].get('data-total-page'))
			return total_page
		except urllib2.URLError as  e:
			if hasattr(e, "reason"):
				print u"连接失败，错误原因", e.reason
				return None
			print e
			print '233'
			return None
	def get_comment(self):
		pageCode = self.get_page()
		total_time = 200
		while pageCode == None and total_time > 0:
			pageCode = self.get_page()
			total_time -= 1
		ret = []
		try:
			'''
			pattern = re.compile('<div xmlns:v=.*?typeof="v:Review".*?<span property="v:rating".*?title="(.*?)"></span>.*?<div class="main-bd">.*?<div class="short-content">(.*?)<a.*?</a>', re.S)
			items = re.findall(pattern, pageCode)
			for item in items:
                ret.append('评分：' + item[0] + '\n' + '评价：' + item[1] + '\n')
            return ret
			'''
			soup = BeautifulSoup(pageCode, 'lxml')
			#raw_input('---')
			#items = soup.find_all('div xmlns:v=', "v:Review", 'property', "short-content")
			#div class="short-content
			items = soup.find_all('div',attrs={'class':'main review-item'})
			for item in items:
				tag_s = item.find('span',attrs={'property':'v:rating'})
				score = str(tag_s.get('title'))
				#print score
				tag_c = item.find('div',attrs={'class':'short-content'})
				comment = str(tag_c.get_text().strip())
				#print comment
				#raw_input('---')
				ret.append('评分：' + score + '\n' + '评价：' + comment)
			return ret
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"连接失败，错误原因", e.reason
				return None
	def get_page(self):
		socket.setdefaulttimeout(2)
		time.sleep(3+random.randint(0,5))
		try:
			header = self.get_header()
			'''
			request = urllib2.Request(self.URL, headers = header)
			
			random_proxy = self.ippool[random.randint(0,len(self.ippool)-1)]
			print 'run time ',self.run_time
			print header
			print random_proxy
			proxy_support=urllib2.ProxyHandler({"http":random_proxy})
			opener = urllib2.build_opener(proxy_support)
			urllib2.install_opener(opener)
			
			response = urllib2.urlopen(request)
			'''
			print self.ippool[random.randint(0,len(self.ippool)-1)]
			response = requests.get(url = self.URL,headers = header,proxies = {'proxy':'http:\\'+self.ippool[random.randint(0,len(self.ippool)-1)]})
			#print response.text
			#raw_input('----')
			#page = response.read().decode('utf-8')
			page = response.text
			#print page
			return page
		except urllib2.URLError as e:
			if hasattr(e,"reason"):
				print u"连接失败，错误原因", e.reason
				return None
		except socket.timeout as e:
			print type(e)
			return None
	def get_cookie(self):
		c = cookielib.LWPCookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(c))
		login_path = 'https://accounts.douban.com/login?source=movie'
		data = {'name':'MYT0420' , 'passwd': 'ma12238953420'}
		post_info = urllib.urlencode(data)
		request = urllib2.Request(login_path, post_info)
		html = opener.open(request).read()
		if c:
			print c
		return c
	def get_header(self):
		#cookie = self.get_cookie()
		index = random.randint(0,len(self.user_agents)-1)
		agent = self.user_agents[index]
		#header = {'User-Agent': agent, 'cookie': cookie}
		header = {'User-Agent':agent}
		return header
spider = CrawlComment()
Num = spider.get_comment_Num()
print Num
title = spider.get_title()
print title
indexs = []
for index in range(Num):
	indexs.append(index)
random.shuffle(indexs)
#print indexs
for index in indexs:
	spider.setPage(index)
	print 'index:',index
	spider.run_time += 1
	comment = spider.get_comment()
	saveFile(title, index)
	saveFile(comment, index)
