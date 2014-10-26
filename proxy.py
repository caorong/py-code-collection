# coding: utf-8

import requests, time,datetime, re, sets, sys, os
from subprocess import Popen, PIPE

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
}

qp_proxy_add = 'http://www.site-digger.com/html/articles/20110516/proxieslist.html'

proxy_tr = re.compile("(?isu)<tr[^>]*>(.*?)</tr>")
proxy_td = re.compile("(?isu)<td[^>]*>(.*?)</td>")
proxy_ip = re.compile("\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}:\d+")

# proxy set from site-digger and localFile(if has)
proxy_set = sets.Set()

# good proxy which used
good_proxy_set = sets.Set()


def add_last_valid_ip():
    if not  os.path.exists('./last_valid_ip'):
        print 'not exists'
        return 
    with open('last_valid_ip','rb') as f:
        for i in f.xreadlines():
            proxy_set.add(i.strip())

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


if __name__ == "__main__":
    
