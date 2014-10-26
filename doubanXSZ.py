# coding: utf-8

import requests, time,datetime, re, sets, sys, os, random
from subprocess import Popen, PIPE, traceback
import threading, Queue, time
from lxml import etree
from io import StringIO, BytesIO
import json

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
}

qp_proxy_add = 'http://www.site-digger.com/html/articles/20110516/proxieslist.html'

proxy_tr = re.compile("(?isu)<tr[^>]*>(.*?)</tr>")
proxy_td = re.compile("(?isu)<td[^>]*>(.*?)</td>")
proxy_ip = re.compile("\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}:\d+")

DB_XSZ_URL = 'http://www.douban.com/group/haixiuzu/discussion'

# proxy set from site-digger and localFile(if has)
proxy_set = sets.Set()

# good proxy which used
good_proxy_set = sets.Set()


##################################################
# proxy
##################################################

def add_last_valid_ip():
    if not  os.path.exists('./last_valid_ip'):
        print 'not exists'
        return 
    with open('last_valid_ip','rb') as f:
        for i in f.xreadlines():
            proxy_set.add(i.strip())

def store_valid_ip():
    with open('last_valid_ip','wb') as f:
        for ip in good_proxy_set:
            f.write(ip+"\n")

# deprcated
def add_proxy_ip():
    """ add site-digger's ip """
    r = requests.get(qp_proxy_add, headers=headers, timeout=5)
    # print r.text
    for row in proxy_tr.findall(r.text):
        for col in proxy_td.findall(row)[:1]:
            proxy_set.add(col)
    print proxy_set
    print len(proxy_set)

def get_proxy_ip():
    page = req_proxy_page()
    for row in proxy_ip.findall(page) :
        proxy_set.add(row)
    print proxy_set
    print len(proxy_set)

def req_proxy_page():
    p = Popen(['/usr/local/bin/phantomjs', '/Users/caorong/Documents/workspace_py/ptest.js'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    rc = p.returncode
    # print output, err, rc
    if rc is not 0:
        raise Exception('call phantomjs error!')
    return output

def req_ip(proxy_address=None):
    # http://ip.taobao.com/service/getIpInfo2.php?ip=myip
    # req_ip( {'http':"http://"+str(proxy_set.pop())})
    if proxy_address is None:
        r = requests.post('http://ip.taobao.com/service/getIpInfo2.php?ip=myip',\
                headers=headers, timeout=5, proxies=proxy_address)
    else:
        r = requests.post('http://ip.taobao.com/service/getIpInfo2.php?ip=myip',\
                headers=headers, timeout=5, proxies={'http':"http://" + str(proxy_address)})

    print r.content
    return json.loads(r.content)['data']['ip']
    # page = etree.HTML(r.content.decode(r.encoding))
    # content = page.xpath(u"//div[@class='topic-doc']/div/div[@class='topic-content']//img")

def get_a_proxy():
    if len(good_proxy_set) == 0:
        return None
    else:
        return {'http' : "http://" + str(random.sample(good_proxy_set,1))}
    
class CheckValidProxyThread(threading.Thread):
    def __init__(self, inqueue):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.inqueue = inqueue
        self.start()
        print 'proxy check thread start'

    def run(self):
        get_proxy_ip()
        add_last_valid_ip()
        local_ip = req_ip()
        print local_ip
        # print proxy_set.pop()
        # print req_ip( {'http':"http://"+str(proxy_set.pop())})
        for i in proxy_set:
            try:
                rip = req_ip(i)
                if local_ip != rip:
                    # print rip
                    good_proxy_set.add(i)
            except:
                print "catch err", sys.exc_info()[0] 
            time.sleep(0.5) 
        print good_proxy_set
        print 'valid ip finash!!!!'
        store_valid_ip()
        

#########################

def crawler_douban_list():
    '''
    http://www.douban.com/group/haixiuzu/discussion?start=25
    http://www.douban.com/group/haixiuzu/discussion?start=50
    '''
    start = 0
    # r = requests.get(add1, headers=headers, timeout=5, proxies=proxiess)
    while True:
        add1 = DB_XSZ_URL + "?start=" + str(start)
        r = requests.get(add1, headers=headers, timeout=5)
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
        # parse_douban_page(sublinks[0].attrib['href'])

        
def parse_douban_single_page(url):
    # url = 'http://www.douban.com/group/topic/64777974'
    # TODO make request tobe a  Thread Task
    r = requests.get(url, headers=headers, timeout=5, proxies=get_a_proxy())
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
    CheckValidProxyThread(None)
    time.sleep(10000)
    # crawler_douban_list()
    
def teststr():
    str1 = 'http://qqq/123123.jpg'
    # print dir(str)
    print str1[str1.rindex('/')+1:] 


def test_thread():
    queue1 = Queue.Queue(4)
    CheckValidProxyThread(queue1)

if __name__ == "__main__":
    # req_proxy_page()
    # get_proxy_ip()
    start()
    # teststr()
    # req_ip()
    # test_thread()
    # time.sleep(22)

