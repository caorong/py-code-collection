# coding: utf-8

import os
from subprocess import Popen, PIPE, traceback

PHANTOMJS_PATH = ''

def setPhantomJsPath(path):
    """
    set custom PHANTOMJS_PATH 
    """
    if not path.endswith('phantomjs'):
        path += os.sep + 'phantomjs'
    global PHANTOMJS_PATH 
    PHANTOMJS_PATH = path

def checkPath():
    global PHANTOMJS_PATH 
    if os.path.isfile('/usr/local/bin/phantomjs'):
        PHANTOMJS_PATH = '/usr/local/bin/phantomjs'
    elif os.path.isfile('/usr/bin/phantomjs'):
        PHANTOMJS_PATH = '/usr/bin/phantomjs'
    if not os.path.isfile(PHANTOMJS_PATH):
        raise Exception('phantomjs not exist with path ' + PHANTOMJS_PATH +\
                'use setPhantomJsPath to set Path')

def req_page(jsFile):
    global PHANTOMJS_PATH 
    if PHANTOMJS_PATH == '':
        checkPath()
    print 'jsfile is {}'.format(jsFile)
    p = Popen([PHANTOMJS_PATH, jsFile], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    rc = p.returncode
    # print output, err, rc
    if rc is not 0:
        raise Exception('call phantomjs error!')
    return output

if __name__ == "__main__":
    # setPhantomJsPath('/usr/local/bin')
    # checkPath()
    print req_page('./site-digger.js')
