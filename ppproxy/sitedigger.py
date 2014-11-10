# coding: utf-8

import phantomjs
from parser import BaseParser
import re, sys, os

"""
This module will use phantomjs to request site-digger
"""

SITE_DIGGER = 'http://www.site-digger.com/html/articles/20110516/proxieslist.html'

class SiteDiggerParser(BaseParser):
    
    def test(self):
        print super(SiteDiggerParser, self).printtest()
        self.printtest()

    def parse(self):
        # find the current file path http://stackoverflow.com/questions/4934806/python-how-to-find-scripts-directory 
        # print os.path.dirname(os.path.realpath(__file__)) 
        page = phantomjs.req_page(os.path.join(os.path.dirname(\
                os.path.realpath(__file__)), 'site-digger.js'))
    
        proxy_ip = re.compile("\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}:\d+")
        for row in proxy_ip.findall(page) :
            # self.proxy_set.add(row)
            self.put(row)
        # super(SiteDiggerParser, self).printtest()       
        
if __name__ == "__main__":
    import Queue
    sdp = SiteDiggerParser(Queue.Queue(10000))
    print sdp
    # sdp.test()
    sdp.parse()
