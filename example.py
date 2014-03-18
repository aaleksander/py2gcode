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
    #m = Meta()
    #m.point(0, 0)
    #m.point(100, 0)
    #m.point(100, 100)
    #m.point(0, 100)
    #m.jump_point(5, [10, 90, 40, 60])

    str = "m 163.64471,339.19449 c 2.02031,12.12183 111.85126,22.79881 141.42136,161.6244 14.31254,67.19447 52.6657,46.06442 32.92713,-1.08194 0,0 -57.17079,-142.35972 9.49928,-160.54246 66.67006,-18.18275 -96.97465,-82.83251 -96.97465,-82.83251 z"
    svg = SvgTrajectory(str)
    svg.to_zero()
    o = Offset(svg, -10)
    o.jump_point(15, [10, 80])
    #preview2D([o], 3, options={'hideRef': True})
	
    G0(0, 0, 5)
    c = Strategy()
    c.cut_on_line(o, -2, -10, 3, 5, Tool())

def f2():
    G0(0, 0, 5)
    font = get_font("arial")
    t = TextTrajectory(font, "Иван Вячеславович")
    sz = 5
    t.grav(0, 0, -1, sz, 500, 3)


print("g21 g64 g90")
preview(f)
#export(f2)
