#!/usr/bin/env python
#-*-coding:utf8-*-import re
import urllib2
from urlparse import urlparse
from bs4 import BeautifulSoup as bs


result = open('result.txt','wb')
#定义一个头信息
def site_hdr(site): 
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	       'Accept-Encoding': 'none',
	       'Accept-Language': 'en-US,en;q=0.8',
	       'Connection': 'keep-alive'}
	request = urllib2.Request(site, headers = hdr)	
	page = urllib2.urlopen(request).read()
	return page

#找到title
def find_title(page):
	soup = bs(page, 'html.parser')
	t = soup.find('div', 'padded').find('table')
	res_t = ''
	res = []
	for t1 in t.find_all('th') :
	    res.append(t1.get_text().encode('utf-8'))
#	res.insert(2,'added time')
	res_t = ','.join(res)+'\n'
	return res_t

#找到指定页面的内容
def find_cont(page):
	soup = bs(page, 'html.parser')	
	t = soup.find('div', 'padded').find('table')
	res_cont = ''
	res = []
	for t2 in t.find_all('tr'):
		if t2.find_all('th'):
			continue
		else:
			res = []
			for t3 in t2.find_all('td'):
				res.append(t3.get_text().encode('utf-8'))
			res_cont += ','.join(res)+'\n'
	return res_cont

#翻页（网页，页码）
def jump_next(site, times):
	#找到第一个页面的title和内容
	p = site_hdr(site)
	cont = find_title(p)
	cont += find_cont(p)

	#给循环赋初值
	i = 1
	page = p

	while i < times:
		soup = bs(page, 'html.parser')	
		next_button = soup.find('a', text = 'Older >')
		next_page_site = 'http://www.phishtank.com/phish_archive.php%s' %next_button['href']
	#	print next_page_site
		page = site_hdr(next_page_site)
		cont += find_cont(page)
		i = i+1
	return cont
	
s = '...'
result.write(jump_next(s,3)
result.close()


print 'Here is an end'	
