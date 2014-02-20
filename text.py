#-*- coding: utf-8 -*-

from py2gcode import *
from py2gcode.Fonts import arial

sz = 12
def f():
    G0(0, 0, sz)
    font = get_font("arial")
    t = TextTrajectory(font, "И в а н  В я ч е с л а в о в и ч")
    #for tt in t.trajectories:
    #    tt['svg'].mirror_y()
    t.grav(0, 8.75, 0, sz, 500, 0.8) #0.4
    G0(Z=sz)
    G0(0, 0)

preview(f)
export(f)
    
