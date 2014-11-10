# coding: utf-8

from ppproxy import getProxy
from subprocess import Popen, PIPE, traceback
import requests, datetime, re, sets, sys, os, random
import Queue, time, json
from lxml import etree
from io import StringIO, BytesIO

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
}

DB_XSZ_URL = 'http://www.douban.com/group/haixiuzu/discussion'

def get_a_proxy(proxy):
    return {'http' : "http://" + proxy}

def crawler_douban_list():
    '''
    http://www.douban.com/group/haixiuzu/discussion?start=25
    http://www.douban.com/group/haixiuzu/discussion?start=50
    '''
    start = 0
    # r = requests.get(add1, headers=headers, timeout=5, proxies=proxiess)
    while True:
        add1 = DB_XSZ_URL + "?start=" + str(start)
        print add1
        r = None
        with getProxy() as proxy:
            r = requests.get(add1, headers=headers, timeout=5, proxies=get_a_proxy(proxy))
        if r == None:
            continue
        start += 25
        print r.encoding
        # print r.content
        page = etree.HTML(r.content.decode(r.encoding))
        sublinks = page.xpath(u"//table[@class='olt']/tr/td[@class='title']/a")
        print sublinks
        for i in sublinks:
            # print i.attrib
            try:
                parse_douban_single_page(i.attrib['href'])
            except:
                print i.attrib['href']
                print "catch err", sys.exc_info()[0] 
                print traceback.print_exc()
        time.sleep(2)

def parse_douban_single_page(url):
    # url = 'http://www.douban.com/group/topic/64777974'
    # TODO make request tobe a  Thread Task
    r = None
    with getProxy() as proxy:
        r = requests.get(url, headers=headers, timeout=5, proxies=get_a_proxy(proxy))
    # print r.content
    page = etree.HTML(r.content.decode(r.encoding))
    content = page.xpath(u"//div[@class='topic-doc']/div/div[@class='topic-content']//img")
    print url, 'count = {}'.format(len(content))
    for i in content:
        # print i.attrib['src']
        download_file(i.attrib['src'])
    
def download_file(url, dirname = 'temp'):
    r = requests.get(url, headers=headers, timeout=5)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    filename = url[url.rindex('/') + 1:]
    # do not download twice
    if os.path.isfile(dirname + '/' + filename):
        return
    with open(dirname + '/' + filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return filename



def start():
    crawler_douban_list()

if __name__ == "__main__":
    start()
