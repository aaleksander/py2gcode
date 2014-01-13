# -*- coding: utf-8 -*-
from py2gcode import *

v = Meta()
#v.point(10, 10, 5)
#v.point(40, 10, 5)
#v.point(40, 30, 5)
#v.point(30, 20, -5)
#v.point(20, 20, -5)
#v.point(10, 30, 5)
v.point(50, 10, 10)
v.point(70, 80, -10)
v.point(100, 100, 10)
v.point(70, 120, -10)
v.point(50, 190, 10)
v.point(30, 100, 30)

#v.show(5)

def f():
	G0(0, 0, 5)
	G0(Z = 5)
	z = -3
	while z > -10:
		v.to_gcode(z)
		z -= 1

preview(f)