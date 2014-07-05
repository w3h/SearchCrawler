#!/usr/bin/env python
#coding=utf-8

import urllib2
from lib.search.xgoogle.search import GoogleSearch,SearchResult
from lib.search.baidu.search import BaiduSearch,SearchResult
import socket
import urlparse
import os
import sys
from lib.utils.seo import Seo
import re


result_filename = './output/fckeditor-spider-result.txt'
scaned_filename = './output/fckeditor-spider-scaned.txt'

def banner():
  print '''
|-------------------------------------------------------------------|
| [*] Search backup file  by HHH QQ:2969192549                      |
|-------------------------------------------------------------------|
        '''

def usage():
  if len(sys.argv) < 2 or sys.argv[1].strip() is None:
    print ''
    print 'Usage:' 
    print '  python crack.py [search] '
    print ''
    sys.exit(1)


def unRedirectUrl(url):
    class SimpleRedirectHandler(urllib2.HTTPRedirectHandler):
        def http_error_301(self, req, response, code, msg, headers):
            raise
    
        http_error_302 = http_error_303 = http_error_307 = http_error_301
        http_error_404 = http_error_301
        
    socket.setdefaulttimeout(20)
    req = urllib2.Request(url)
    debug_handler = urllib2.HTTPHandler(debuglevel = 0)
    opener = urllib2.build_opener(debug_handler, SimpleRedirectHandler)
    content = False
    ret = {}

    try:
        response = opener.open(req)
        info = response.read()
        response.close()

        retsearch = re.findall(r"Version.*?,",info)
        if len(retsearch) < 2:
            return ""

        ret['url'] = url
        ret["version"] = "".join(retsearch)

        seoinfo = Seo(url).getInfo() 
        ret["pr"] = seoinfo['pr']
        ret["name"] = seoinfo['name']
    except Exception,e:
        #print '[*] %s' % e
        pass
        
    return ret


def comname(infos):
    res = []
    infolen = len(infos)
    for sp in range(infolen):
        for pos in range(infolen):
            if pos+sp+1 > infolen:
                break

            tmps = infos[pos : pos+sp+1]
            tmp = '.'.join(tmps)
            res.append(tmp)
    return res


def scanList(url):
    retlist = []
    if not 'fckeditor' in url:
        return retlist

    res = urlparse.urlparse(url)
    hosturl = res.scheme + '://' + res.netloc

    if not os.path.isfile(scaned_filename):
        with open(scaned_filename, 'w') as fp: pass
    with open(scaned_filename, 'r') as fp:
        for line in fp.readlines():
            if res.netloc in line:
                return retlist
    with open(scaned_filename, 'a') as fp: fp.write(hosturl + '\n')   

    index = url.find("fckeditor")
    scanurl = url[:index+len("fckeditor")] + "/editor/js/fckeditorcode_gecko.js"
    retlist.append(scanurl)
    return retlist

# write result to file
def writelog(info):
    url = ''
    if not info: return
    if info.has_key('url'): url = info['url']
    if url is None: return

    googlepr = 'unkown'
    baidupr = 'unkown'
    if info.has_key('pr') and info['pr'].has_key('google'): googlepr = info['pr']['google']
    if info.has_key('pr') and info['pr'].has_key('baidu'): baidupr = info['pr']['baidu']

    name = 'unkown'
    if info.has_key('name'): name = info['name']
    
    contentlen = 'unkown'
    if info.has_key('version'): contentlen = info['version']

    infoformat = "[URL] %-50s [VERSION] %-10s [PR-G] %-2s [PR-B] %-2s [name] %s \n" % (url, contentlen , googlepr, baidupr, name)
    with open(result_filename, 'a') as fp: fp.write(infoformat)


def exploit(payload, **kwargs):
    socket.setdefaulttimeout(10)
    scanlist = scanList(payload)
    
    for url in scanlist:
        print "    [-] %s " % url
        r = unRedirectUrl(url)
        if r == '':
            continue
        else:
            writelog(r)
            break

def main():
    banner()    
    usage()

    #gs = GoogleSearch(sys.argv[1].strip())
    #gs.results_per_page = 100

    bs = BaiduSearch(sys.argv[1].strip())
    bs.results_per_page = 100
    lasturlstr = ''
    scanpages = 0

    for index in range(1000000):
        bs.page = index + 1
        results = bs.get_results()

        currurlstr = ''
        for result in results:
            currurlstr += result.getURL()
        if lasturlstr == currurlstr:
            print "[+] Finish the scan! The number of pages is %d." % scanpages
            print ''
            break

        lasturlstr = currurlstr
        for result in results:
            print '[+] %s' % result.getURL()
            exploit(result.getURL())
            scanpages += 1

if __name__ == "__main__":
    #exploit('http://www.jinglawyer.com')
    #url = scanList('http://www.wansent.com/new/fckeditor/editor/filemanager/UploadFiles/image/%E4%B8%87%E7%9B%9B%E6%9C%8D%E5%8A%A1/')
    #print url
    #ret = unRedirectUrl(url)
    #print ret
    #writelog(ret)
    main()
