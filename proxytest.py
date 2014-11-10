# coding: utf-8

# import ppproxy
from ppproxy import getProxy
import Queue, time

def test2():
    q = Queue.Queue(2999)
    q.put_nowait(1)
    q.put_nowait(2)
    q.put_nowait(3)
    print q.get()
    q.put_nowait(4)
    print q.get()

def test():
    # print dir(ppproxy.parser)
    # print ppproxy.parser.checkPath()
    with getProxy() as proxy:
        print 11111
        print proxy
    try:
        with getProxy() as proxy:
            print 222
            print proxy
            raise Exception('1123123')
    except:
        pass

    print 'client exit'

class AbstractClass(object):

 def first(self):
     pass
  
 def second(self):
     pass
  
class ConcreteClass(AbstractClass):

 def first(self):
     print self.__class__.__name__

if __name__ == '__main__':
    # test2()
    test()
    time.sleep(66)
    # obj = ConcreteClass()
    # obj.first()
