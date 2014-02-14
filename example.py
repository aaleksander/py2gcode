# -*- coding: utf-8 -*-

#подключаем библиотеку
from py2gcode import *
from py2gcode.Fonts import arial

def drill(x, y):
	G0(X=x, Y=y, Z=-1)
	for z in xrange(0, 10):
		circle(x, y, z, 2)	
	G0(Z=-20)

#вырежем решетку
def f():
    m = Meta()
    m.point(0, 0)
    m.point(100, 0)
    m.point(100, 100)
    m.point(0, 100)
    m.jump_point(5, [10, 90, 40, 60])

    G0(0, 0, 5)
    c = Strategy()
    c.cut_on_line(m, -5, -10, 1, 5, Tool())


def f2():
    G0(0, 0, 5)
    font = get_font("arial")
    t = TextTrajectory(font, "Иван Вячеславович")
    sz = 5
    t.grav(0, 0, -1, sz, 500, 3)

    '''
    G0(0, 0)
    x1, y1, x2, y2 = t.get_rect(0, 0, 3)
    G0(x1, y1)
    G1(Z=-1)
    G1(x2, y1)
    G1(x2, y2)
    G1(x1, y2)
    G1(x1, y1)
    '''
    

print("g21 g64 g90")
preview(f2)
#export(f2)
