# -*- coding: utf-8 -*-


from py2gcode import *

pp = []
pp.append( point(10, 10, 3) )
pp.append( point(40, 10, 3) )
pp.append( point(40, 30, 3) )
pp.append( point(30, 20, -3) )
pp.append( point(10, 30, 3) )

v = Meta(pp)
#v.show()

def f():	
	G0(0, 0, 5)
	G0(Z = 5)
	z = -3
	while z > -10:
		v.to_gcode(z)
		z -= 1
	
preview(f)