# -*- coding: utf-8 -*-

#подключаем библиотеку
from py2gcode import *


def drill(x, y):
	G0(X=x, Y=y, Z=-1)
	for z in xrange(0, 10):
		circle(x, y, z, 2)	
	G0(Z=-20)

def cut(x1, y1, x2, y2, z1, z2, step):
	'прорезает щель с постепенным погружением'
	G1(X=x1, Y=y1, Z=z1)
	for z in xrange(z1, z2, step*2):
		G1(Z=z + step/2)
		G1(X=x2, Y=y2)
		G1(Z = z + step)
		G1(x1, y1)

#вырежем решетку
def f():
	G0(X=0, Y=0, Z=-20)
	for z in xrange(0, 10, 3):
		rect(0, 0, 100, 60, z)

	G0(Z = -20)
	G0(X=10, Y=10, Z=-5)
	for x in xrange(10, 100, 10):
		G0(X=x, Y=10, Z=-5)
		cut(x, 20, x, 50, 0, 10, 1)
		G0(Z = -5)

	drill(10, 10)
	drill(90, 10)
	drill(90, 60)
	drill(10, 60)

preview(f)
