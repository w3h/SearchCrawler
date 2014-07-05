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


filetype = ['.rar','.zip','.tar.gz']
svntype = [] #['.svn/entries']
scanname = ['www', 'web', 'wwwroot', 'Website', 'website', 'webroot', 'Webroot', '1', '123', '123456', 'cn', 'com', 'org', 'net']
result_filename = './output/backup-spider-result.txt'
scaned_filename = './output/backup-spider-scaned.txt'

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
     
    try:
        response = opener.open(req)
        contentlen = int(dict(response.headers).get('content-length', 0).strip())
        response.close()

        #print contentlen
        if contentlen < 20000:
            return ''
        seoinfo = Seo(url).getInfo() 
        return {"url" : url, "len" : contentlen, 'pr':seoinfo['pr'], 'name' : seoinfo['name']}
    except Exception,e:
        #print '[*] %s' % e
        pass
        
    return ''


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


def scanBackupList(url):
    res = urlparse.urlparse(url)
    hosturl = res.scheme + '://' + res.netloc
    backuplist = []

    if res.netloc == '': return backuplist
    if not os.path.isfile(scaned_filename):
        with open(scaned_filename, 'w') as fp: pass
    with open(scaned_filename, 'r') as fp:
        for line in fp.readlines():
            if res.netloc in line:
                return ''
    with open(scaned_filename, 'a') as fp: fp.write(hosturl + '\n')
        
    for index in svntype:
        backuplist.append(hosturl + '/' + index)

    comnames = comname(res.netloc.split('.'))
    for ft in filetype:
        for name in scanname:
            backuplist.append(hosturl + '/' + name + ft)

        for path in comnames:
            backuplist.append(hosturl + '/' + path + ft)
    return backuplist


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
    if info.has_key('len'): contentlen = info['len']

    infoformat = "[URL] %-50s [LEN] %-10s [PR-G] %-2s [PR-B] %-2s [name] %s \n" % (url, contentlen , googlepr, baidupr, name)
    with open(result_filename, 'a') as fp: fp.write(infoformat)


def exploit(payload, **kwargs):
    socket.setdefaulttimeout(10)
    scanlist = scanBackupList(payload)
    
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

    gs = GoogleSearch(sys.argv[1].strip())
    gs.results_per_page = 100
    lasturlstr = ''
    scanpages = 0

    for index in range(1000000):
        gs.page = index + 1
        results = gs.get_results()

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
    #ret = unRedirectUrl('http://www.tegoshiyuya.cn/www.rar')
    #print ret
    #writelog(ret)
    main()
