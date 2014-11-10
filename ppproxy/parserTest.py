# coding: utf-8

import unittest
import phantomjs

class PhantomJsTest(unittest.TestCase):
    def checkPath(self):
        phantomjs.checkPath()

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(PhantomJsTest('checkPath'))
    
    runner = unittest.TextTestRunner()
    runner.run(suite)
