# -*- coding: utf-8 -*-

from py2gcode import *



def go_home():
	G0(Z=0)
	G0(X=0, Y=0, Z=0)

@cnc
def f():
	go_home()


#export(f, 'test.nc')
preview(f)

