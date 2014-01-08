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
	G0(X=0, Y=0, Z=0)

	dep = -4

	while dep > -9:
		G1(Z= dep)

		for x in xrange(3, 45, 6):
			G1(Y=75)
			G1(X=x)
			G1(Y=0)
			G1(X=x + 3)		
		G1(Y=75)
		G1(X=0)
		G0(Z=0)
		G0(X=42, Y=0)
		G1(Z=dep)
		G1(X=0)
		dep -= 1
	G0(0, 0, 0)

print("g21 g64 g90")
print("F200")
export(f)

print "M2"
