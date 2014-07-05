#coding=utf-8
import re,hashlib,chardet
from HTMLParser import HTMLParser
import lxml.html.soupparser as soupparser


def decode(info, newcode='utf-8'):
    enc = chardet.detect(info)['encoding']
    info = info.decode(enc).encode(newcode)
    return info


def strip_tags(html):
    html = html.strip()
    html = html.strip("\n")
    result = []
    parse = HTMLParser()
    parse.handle_data = result.append
    parse.feed(html)
    parse.close()
    return "".join(result)


def xpath(info, path):
    return soupparser.fromstring(info).xpath(path) 

