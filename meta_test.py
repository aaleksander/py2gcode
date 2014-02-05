# -*- coding: utf-8 -*-
from py2gcode import *

v = Meta()
v.point(20, 20,  rounding=3)
v.point(30, 20,  rounding=3)
v.point(30, 10,  rounding=3)
v.point(45, 20,  radius=-3)
v.point(60, 10,  radius=5)
v.point(65, 40)
v.point(20, 40,  rounding=3)

v.jump_point(5, [15, 50, 70])
v.show(8)

v2 = Meta()
v2.point(30, 32, radius=3)
v2.point(50, 32, radius=5)
v2.jump_point(5, [15, 65])
v2.show(8)

def f():
    G0(0, 0, 5)
    G0(Z = 5)
    F(1000)


    x,  y =  v2.get_first_position()
    G0(x, y)    
    z = -3
    while z > -10:
    	G1(Z=z)
        v2.to_gcode(z, -8)
        z -= 2
    G0(Z=5)

    x,  y =  v.get_first_position()
    G0(x, y)    
    z = -3
    while z > -10:
    	G1(Z=z)
        v.to_gcode(z, -8)
        z -= 2

preview(f)

#export(f)
