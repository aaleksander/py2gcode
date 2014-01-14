# -*- coding: utf-8 -*-
from py2gcode import *

v = Meta()
v.point(100, 100, 20)
v.point(200, 70, 50)

#v.point(30, 100, 10)
#v.point(100, 100, 80)
#v.point(100, 30, 10)
#v.point(100, 100, -60)

#v.point(10, 10, 5)
#v.point(40, 10, 5)
#v.point(40, 30, 5)
#v.point(30, 20, -5)
#v.point(20, 20, -5)
#v.point(10, 30, 5)



v.show(3)

def f():
	G0(0, 0, 5)
	G0(Z = 5)
	z = -3
	while z > -10:
		v.to_gcode(z)
		z -= 2


preview(f)