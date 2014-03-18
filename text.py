#-*- coding: utf-8 -*-

from py2gcode import *
from py2gcode.Fonts import arial

sz = 5
def f():
    G0(0, 0, sz)
    font = get_font("arial")
    t = TextTrajectory(font, "Проба текста")
    t.grav(0, 0, 0, sz, 500, 2.8) #0.4
    G0(Z=sz)

#preview(f)
export(f)
