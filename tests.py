# -*- coding: utf-8 -*-

from py2gcode import *
import unittest



class TestGCodes(unittest.TestCase):
    def setUp(self):
        pass

    def test_G0(self):
    	clearCNC()
    	f = cnc(lambda: G0(X=1))
    	res = f()

    	self.assertTrue(res == "G0 X1")

    	clearCNC()
    	f = cnc(lambda: G0(X=1, Y=2, Z=3))
    	self.assertTrue(f() == "G0 X1 Y2 Z3")

    def test_G1(self):
    	clearCNC()
    	f = cnc(lambda: G1(X=1))
    	res = f()

    	self.assertTrue(res == "G1 X1")

    	clearCNC()
    	f = cnc(lambda: G1(X=1, Y=2, Z=3))
    	self.assertTrue(f() == "G1 X1 Y2 Z3")


if __name__ == '__main__':
    unittest.main()


'''
@cnc
def f():
	G0(X=0)

print f()
'''
