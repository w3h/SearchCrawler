#coding=utf-8
import urllib2
import urlparse
import html
import random

BROWSERS = (
    # Top most popular browsers in my access.log on 2009.02.12
    # tail -50000 access.log |
    #  awk -F\" '{B[$6]++} END { for (b in B) { print B[b] ": " b } }' |
    #  sort -rn |
    #  head -20
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.6) Gecko/2009011912 Firefox/3.0.6',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6 (.NET CLR 3.5.30729)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6 (.NET CLR 3.5.30729)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.48 Safari/525.19',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
    'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.5) Gecko/2008121621 Ubuntu/8.04 (hardy) Firefox/3.0.5',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-us) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Baiduspider (http://www.baidu.com/search/spider.htm)',
)

class Seo:
    def __init__(self, url):
        self.url = url
        self.urlpara = urlparse.urlparse(url)
        self.info = {}

    def getHtml(self, url, xpathsearch = None):
        try:
            print url
            request = urllib2.Request(url)
            request.add_header('User-Agent', random.choice(BROWSERS))
            ul = urllib2.urlopen(request)
            info = ''.join(ul.read())
            if info is None:
                return ""

            r = html.xpath(info, xpathsearch)
            return ''.join(r).strip()
        except Exception,e:
            print '[*] %s' % e  
    
        return ""

    def getGooglePR(self):
        url = r"http://pr.alexa.cn/?url=" + self.urlpara.netloc
        xp = r"//body/div[1]/div[2]/div/ul/li[1]/span/text()"
        return self.getHtml(url, xp)

    def getBaiduPR(self):
        url = r"http://mytool.chinaz.com/baidusort.aspx?host=" + self.urlpara.netloc
        xp = r".//*[@id='main']/div/div[1]/div/div/div/div/div[2]/div/div/div[1]/font[1]/text()"
        return self.getHtml(url, xp)

    def getInfo(self):
        url =  self.urlpara.scheme + r'://' + self.urlpara.netloc
        xp = r".//title/text()"
        r = self.getHtml(url, xp)

        self.info['name'] = ''.join(r)
        self.info['pr'] = {"google" : self.getGooglePR(), "baidu" : self.getBaiduPR()}
        return self.info


if __name__ == "__main__":
    seo = Seo('http://www.souoa.com/www.rar')
    print seo.getInfo()
