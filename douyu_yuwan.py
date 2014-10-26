# coding: utf-8

import requests, time,datetime, re, sets, sys, os

proxies = {
  # "http": "http://115.29.166.133:82",
  # "http": "http://119.31.123.207:8000",
  # "http": "http://120.198.230.16:80",
  # "http": "http://120.198.230.17:80",
  # "http": "http://220.181.32.106:80",
  # "http": "http://113.196.34.66:8080",
  "http": "http://37.239.46.18:80",
}

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
}


test_address = 'http://192.243.117.62:8888'
qp_proxy_add = 'http://www.site-digger.com/html/articles/20110516/proxieslist.html'


dy_watched_uids = [50596, 2813]
# dy_address1 = 'http://www.douyutv.com/50596?fromuid=1641651'
# dy_address = 'http://www.douyutv.com/specific/get_room_show/50596?fromuid=1641651&_='
dy_address1 = 'http://www.douyutv.com/{uid}?fromuid=1641651'
dy_address = 'http://www.douyutv.com/specific/get_room_show/{uid}?fromuid=1641651&_='


proxy_tr = re.compile("(?isu)<tr[^>]*>(.*?)</tr>")
proxy_td = re.compile("(?isu)<td[^>]*>(.*?)</td>")

# proxy set from site-digger and localFile(if has)
proxy_set = sets.Set()

# good proxy which used
good_proxy_set = sets.Set()

def test_go():
    r = requests.get(test_address, headers=headers,proxies=proxies, timeout=5)
    print r.text
   
def test_c_proxy():
    """ add site-digger's ip """
    r = requests.get(qp_proxy_add, headers=headers, timeout=5)
    # print r.text
    for row in proxy_tr.findall(r.text):
        for col in proxy_td.findall(row)[:1]:
            # print col
            proxy_set.add(col)
    print proxy_set
    print len(proxy_set)

def test_douyu():
    for i in dy_watched_uids:
        add1 = dy_address1.replace('{uid}',str(i))
        add2 = dy_address.replace('{uid}',str(i))
        r = requests.get(add1, headers=headers, timeout=5, proxies=proxies)
        print r.status_code
        r = requests.get(add2 + str(g_tsp()), headers=headers, timeout=5, proxies=proxies)
        print add2 + str(g_tsp())
        if r.text.startswith("{\"owner_weight\":"):
            good_proxy_set.add(proxies.get('http'))
        print r.text
        print good_proxy_set
        time.sleep(2)

def req_douyu(proxiess):
    for i in dy_watched_uids:
        add1 = dy_address1.replace('{uid}',str(i))
        add2 = dy_address.replace('{uid}',str(i))
        try:
            r = requests.get(add1, headers=headers, timeout=5, proxies=proxiess)
            print r.status_code
            r = requests.get(add2 + str(g_tsp()), headers=headers, timeout=5, proxies=proxiess)
            print add2 + str(g_tsp())
            print r.text
            if r.text.startswith("{\"owner_weight\":"):
                good_proxy_set.add(proxiess.get('http'))
            time.sleep(2)
        except: #error as (errno, strerror):
            print "catch err", sys.exc_info()[0]
            # print "error{0}: {1}".format(errno, strerror)

def test_local_file():
    add_last_valid_ip()
    print proxy_set
    # test_c_proxy()
    for i in proxy_set:
        good_proxy_set.add(i)
    store_valid_ip()

def begin_douyu():
    test_c_proxy()
    add_last_valid_ip()
    for ad in proxy_set:
        req_douyu({'http':"http://"+str(ad)})
        time.sleep(3)
    store_valid_ip()

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

def g_tsp():
    return int(time.time()*1000)

def test_timestamp():
    print int(time.time()*1000)
    print datetime.datetime.fromtimestamp(int(1408882497226/1000)).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    # test_timestamp()
    # test_go()
    # test_douyu()
    # test_c_proxy()
    # test_local_file()
    begin_douyu()
