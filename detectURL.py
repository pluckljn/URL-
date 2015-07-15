#!/usr/bin/env python
#-*-coding:utf8-*-
#查询Alexa前100万排名的网站中是否有HFS,nginx,IIS,Apache站点
import urllib2
import re
from bs4 import BeautifulSoup as bs
import socket
import urlparse
import codecs
import ssl

f = codecs.open('top.txt','rb',encoding = 'utf-16') #Alexa top1m的查询
#fs = open('sites.txt', 'rb')  #之前给出的site的查询

a = open('output.txt','wb')
output = ''



def detectURL(site,retries = 2) :
    socket.setdefaulttimeout(6)
    hdr ={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'}
    request = urllib2.Request(site, headers = hdr)
    try:
        page = urllib2.urlopen(request)
        content = page.read()
        return detectWebSite(content)
    except Exception, err:
        print err
        try:
            content = err.read()
            return detectWebSite(content)
        except Exception:
            if retries > 0:
                return detectURL(site, retries-1)
            else:
                print 'Here is an error'
                return 'error'

def  detectWebSite(content):
    soup = bs(content,'html.parser')
    
    site_HFS = soup.find_all('a',text = re.compile(".*HttpFileServer.*")) and (
               soup.find_all('title',text = '信息中心 /')  or \
               soup.find_all('title',text = 'HFS /')  )
                   
    site_Apache = soup.find_all('p',text = re.compile('.*Apache.*')) and (
                  soup.find_all('title',text = 'Apache HTTP Server Test Page powered by CentOS') or \
                  soup.find_all('title', text = 'Test Page for the Apache HTTP Server on Fedora')  )
    
    site_IIS = soup.find_all('title', text = '建设中') and \
               soup.find_all('h5',text = re.compile(".*IIS.*"))
    
    site_nginx = soup.find_all('center', text = re.compile(".*nginx.*")) and \
                 soup.find_all('title', text = '403 Forbidden')

    #(1)判断HFS的登录页面
    if site_HFS:
        print  'This is a HFS login site' #%site.strip()
        return 'HFS'

    #(2)判断Apache的页面
    elif site_Apache:
        print 'This is an Apache site' #%site.strip()
        return 'Apache'
                        
    #(3)判断IIS的页面
    elif site_IIS:
        print 'This is a IIS site' #%site.strip()
        return 'IIS'

    #(4)判断nginx的页面
    elif site_nginx:
        print 'This is a nginx site' #%site.strip()
        return 'nginx'
    else:
        print 'This is not a HFS,Apache,IIS,nginx site'
        return 'Null'

#Alexa top1m的查询
try:
    for s in range (1000000):
        s =f.readline()
        c = 'http://' 
        link = c+s
        res = detectURL(link)
        print link
        output += '%s|%s\n'  %(link.strip(),res)
except StopIteration:
        print 'Here is an end'
print output
a.write(output)

f.close()
a.close()

'''

#之前给出的site的查询
try:
    link = fs.readline()
    while link:
        res = detectURL(link)
        output += '%s|%s\n'  %(link.strip(),res)
        link = fs.next()
except StopIteration:
    print 'Here is an end'
print output
a.write(output)

fs.close()
a.close()
'''
