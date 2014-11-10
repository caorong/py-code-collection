# coding: utf-8

import sets, Queue, time
import ppproxy
from kuaidaili import KuaidlParser
from sitedigger import SiteDiggerParser
from parser import ProxyCheckThread, MonitorThread

__version__ = '0.0.1'

unCheckedIpQueue = Queue.Queue(10000)
checkedIpQueue = Queue.Queue(10000)
usedProxyQueue = Queue.Queue(10000)

def init():
    # start site-digger 
    print 'ppproxy init ...'
    KuaidlParser(unCheckedIpQueue)
    # SiteDiggerParser(unCheckedIpQueue)
    print unCheckedIpQueue.qsize()
    print 'start proxyCheck Thread...'
    MonitorThread(unCheckedIpQueue, checkedIpQueue, usedProxyQueue)
    for i in xrange(3):
        ProxyCheckThread(unCheckedIpQueue, checkedIpQueue)
    # print unCheckedIpQueue.get()

class GetProxyProxy:
    def __enter__(self):
        self.proxy = getCheckedIp()
        return self.proxy
    
    def __exit__(self, type, value, trace):
        print trace
        if trace is None:
            usedProxyQueue.put(self.proxy)

def getProxy():
    return GetProxyProxy()

def getCheckedIp():
    """
    A method will return a anonymous checkedIp and it will return 
    """
    # block version
    if checkedIpQueue.qsize()==0 and usedProxyQueue.qsize()==0:
        c1 = checkedIpQueue.get()
        # usedProxyQueue.put(c1)
        return c1
    # when new ip is empty
    if checkedIpQueue.qsize() == 0:
        u1 = usedProxyQueue.get()
        # usedProxyQueue.put(u1)
        return u1
    else:
        c1 = checkedIpQueue.get()
        # usedProxyQueue.put(c1)
        return c1
    # no blcok verison
    # try:
        # checkedp = checkedIpQueue.get(False)
    # except:
        # checkedp = None
    # if checkedp == None:
        # try:
            # checkedp = usedProxyQueue.get_nowait()
        # except:
            # checkedp = None
    # if checkedp != None:
        # usedProxyQueue.put_nowait(checkedp)
    # return checkedp

init()

