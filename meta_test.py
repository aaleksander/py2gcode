# -*- coding: utf-8 -*-
from py2gcode import *

v = Meta()
v.point(20, 20,  rounding=3)
v.point(30, 20,  rounding=3) 
v.point(30, 10,  rounding=3)
v.point(45, 20,  radius=-3) 
v.point(60, 10,  radius=5) 
v.point(65, 40) 
v.point(20, 40) 

v.show(8)

def f():
    G0(0, 0, 5)
    G0(Z = 5)
    z = -3
    while z > -10:
        v.to_gcode(z)
        z -= 2

preview(f)

#export(f)
