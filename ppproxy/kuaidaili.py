# coding: utf-8

from parser import BaseParser
from lxml import etree
from io import StringIO, BytesIO
import time

# http://www.kuaidaili.com/free/inha/1/ 
KUAI_URL = 'http://www.kuaidaili.com/free/inha/'

class KuaidlParser(BaseParser):

    def parse(self):
        for i in [ x+1 for x in xrange(10)]:
            self.parseInternal(i)
            time.sleep(2)

    def parseInternal(self, no):
        r = super(KuaidlParser, self).fetch(KUAI_URL + str(no))
        page = etree.HTML(r.content.decode(r.encoding))
        trs = page.xpath(u"//table[@class='table table-bordered table-striped']/tbody/tr")
        # print dir(trs[0])
        # print trs[0].xpath(u"td")
        # print dir(trs[0].xpath(u"//td")[0])
        # print trs[0].xpath(u"//td")[0].text
        for i in trs:
            try:
                ip = i.xpath(u"td")[0].text
                port = i.xpath(u"td")[1].text
                # print ip +":"+ port
                # self.proxy_set.add(ip + ":" + port)
                self.put(ip + ":" + port)
            except :
                print "kuaidaili err ", sys.exc_info()[0] 
                print traceback.print_exc()

if __name__ == "__main__":
    kdl = KuaidlParser()
    kdl.parse()
    kdl.printtest()

