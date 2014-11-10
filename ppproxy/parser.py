# coding: utf-8

import sets, Queue, sys, traceback
import requests
import threading, time, json

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
}

"""
base parser  
"""
class BaseParser(object):

    def __init__(self, inqueue):
        self.proxy_set = sets.Set()
        self.unCheckedIpQueue = inqueue
        self.parse()
        # self.checkedIpQueue = Queue.Queue(10000)
        # for i in xrange(3):
            # ProxyCheckThread(self.unCheckedIpQueue, self.checkedIpQueue)

    def parse(self):
        pass

    def put(self, ip_port):
        if ip_port in self.proxy_set:
            pass
        else:
            self.proxy_set.add(ip_port)
            self.unCheckedIpQueue.put(ip_port)
    
    def printtest(self):
        print self.proxy_set

    def fetch(self, url):
        r = requests.get(url, headers=headers, timeout=5)
        # print r.encoding
        return r


class ProxyCollectThread(threading.Thread):
    """
    collect all proxy from which extend BaseParser
    """
    def __init__(self, inqueue, outqueue):
        self.inqueue = inqueue    
        self.outqueu = outqueue
        self.setDaemon(True)

    def run(self):
        pass

class MonitorThread(threading.Thread):
    def __init__(self, inqueue, outqueue, queue3):
        threading.Thread.__init__(self)
        self.inqueue = inqueue
        self.outqueue = outqueue
        self.queue3 = queue3
        self.setDaemon(True)
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            print "uncheckProxySize {}, checkProxySize {}, usedProxySize {}"\
                    .format(self.inqueue.qsize(), self.outqueue.qsize(), \
                    self.queue3.qsize())
            time.sleep(3)

class ProxyCheckThread(threading.Thread):

    def __init__(self, inqueue, outqueue):
        threading.Thread.__init__(self)
        self.inqueue = inqueue
        self.outqueue = outqueue
        self.localip = req_ip()
        # self.daemon = True
        self.setDaemon(True)
        self.daemon = True
        print 'localip => {}'.format(self.localip)
        self.start()

    def run(self):
        while True:
            tmpip = self.inqueue.get()
            print 'now checking {} '.format(tmpip)
            try:
                if self.localip != req_ip(tmpip):
                    print 'valid proxy {}'.format(tmpip)
                    self.outqueue.put(tmpip)
            except :
                print "proxyCheckThread err ", sys.exc_info()[0] 
                # print traceback.print_exc()



def req_ip(proxy_address=None):
    # http://ip.taobao.com/service/getIpInfo2.php?ip=myip
    # req_ip( {'http':"http://"+str(proxy_set.pop())})
    if proxy_address is None:
        r = requests.post('http://ip.taobao.com/service/getIpInfo2.php?ip=myip',\
                headers=headers, timeout=3, proxies=proxy_address)
    else:
        r = requests.post('http://ip.taobao.com/service/getIpInfo2.php?ip=myip',\
                headers=headers, timeout=3, proxies={'http':"http://" + str(proxy_address)})

    return json.loads(r.content)['data']['ip']
    # print 'req_ip => {}'.format(r.content)

    
if __name__ == "__main__":
    bp = BaseParser()
    time.sleep(2)
