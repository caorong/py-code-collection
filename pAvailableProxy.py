from ppproxy import getProxy, showAllCheckedProxy
import time

for i in xrange(100):
    print 1
    time.sleep(1)
    q = showAllCheckedProxy()
    print "============="
    print q.qsize()
    for elem in list(q.queue):
        print "==> ", elem


