#!/usr/bin/env python
#coding=utf-8
import urllib2
import urllib
import socket
import BeautifulSoup
import gzip
import StringIO
import re, random, types
import hashlib
import time
import browser
from browser import Browser, BrowserError
from HTMLParser import HTMLParser

def strip_tags(html):
    html=html.strip()
    html=html.strip("\n")
    result=[]
    parse=HTMLParser()
    parse.handle_data=result.append
    parse.feed(html)
    parse.close()
    return "".join(result)

class SearchResult:
    def __init__(self, url = '', title = '', content = ''):
        self.url = url 
        self.title = title 
        self.content = content

    def getURL(self):
        return self.url

    def setURL(self, url):
        self.url = url 

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getContent(self):
        return self.content

    def setContent(self, content):
        self.content = content

    def __str__(self):
        return '[Baidu]: %s' % self.url

    def printIt(self, prefix = ''):
        print '    url\t->', self.url
        print '  title\t->', self.title
        print 'content\t->', self.content
        print 

    def writeFile(self):
        filename = "result"
        file = open(filename, 'a')
        try:
            file.write('    url:' + self.url+ '\n')
            file.write('  title:' + self.title + '\n')
            file.write('content:' + self.content + '\n\n')

        except IOError, e:
            print 'file error:', e
        finally:
            file.close()

class BaiduSearch(object):
    def __init__(self, query, random_agent=False, debug=False):
        self._page = 1
        self._timeout = 40
        socket.setdefaulttimeout(self._timeout)
        self._beforemd5 = 0
        self._results_per_page = 10
        self._query = query
        self.browser = Browser(debug=debug)

        if random_agent:
            self.browser.set_random_user_agent()

    def get_results(self):
        page = 1
        if self._page > 1:
            page = self._page

        query = urllib2.quote(self._query)
        url = r"http://www.baidu.com/s?wd=%s&tn=baidulocal&pn=%d&rn=%d" % (query, (page - 1) * self._results_per_page, self._results_per_page)
        html = self.browser.get_page(url)
        searchresults = self.extractsearchresults(html)      
        return searchresults

    def _get_page(self):
        return self._page

    def _set_page(self, page):
        self._page = page

    page = property(_get_page, _set_page)

    def _get_results_per_page(self):
        return self._results_per_page

    def _set_results_par_page(self, rpp):
        self._results_per_page = rpp

    results_per_page = property(_get_results_per_page, _set_results_par_page)

    def randomSleep(self):
        sleeptime =  random.randint(120, 240)
        time.sleep(sleeptime)

    #extract the content
    def extractContent(self, info):
        pattern = re.compile(r'(.*?)<br><font color="#008000', re.U | re.M)
        url_match = pattern.search(info)
        if (url_match and url_match.lastindex > 0):
            return url_match.group(1)

        pattern = re.compile(r'(.*?)<br /><font color="#008000">', re.U | re.M)
        url_match = pattern.search(info)
        if (url_match and url_match.lastindex > 0):
            return url_match.group(1)
        else:
            return ''

    def _get_page(self):
        return self._page

    def _set_page(self, page):
        self._page = page

    page = property(_get_page, _set_page)
    
    def checkEndPage(self, infos):
        result = '' 
        for info in infos:
            result += info.getURL()
        
        md5 = hashlib.md5(result)
        if self._beforemd5 != md5.digest():
            self._beforemd5 = md5.digest()
            return False
        else:
            return True

    # extract serach results list from downloaded html file
    def extractsearchresults(self, html):
        results = list()
        soup = BeautifulSoup.BeautifulSoup(html)
        tds = soup.findAll('td', {'class' : 'f'})
        if type(tds) == types.NoneType:
            return types.NoneType
        
        for td in tds:
            link = td.find('a', {'target': '_blank'})
            if (type(link) == types.NoneType):
                continue
            
            url = link['href']
            title = link.renderContents()
            
            content = td.find('font', {'size': '-1'})
            if type(content) == types.NoneType:
                continue

            content = self.extractContent(content.renderContents())            

            result = SearchResult()
            result.setURL(url)
            result.setTitle(strip_tags(title))
            result.setContent(strip_tags(content))
            results.append(result)
        
        return results


def main():
    sea = BaiduSearch('intitle:道德黑客技术论坛内部专版WEBSHELL')
    #sea = BaiduSearch("inurl:Admin_UploadFile.asp")
    results = sea.get_results()
    for link in results:
        print link.getURL()
        print link.getTitle().decode('utf-8').encode('gbk')
        print link.getContent().decode('utf-8').encode('gbk')

if __name__ == "__main__":
    main()

