# -*- coding: utf-8 -*-


from py2gcode import *

#дырки раззенковать

sz = 5 #безопасная Z
def drill(x, y, z1, z2, z3):
	'сверлит отверстие, x, y - центр, z1-z откуда докуда сверлить'
	G0(Z=sz)
	G0(X=x, Y=y)

	#основная дырка
	z = z1
	while z > z2:
		circle(x, y, z, 0.75)	
		z -= 1
	G0(Z=sz)

	#зенковка
	z = z1
	while z > z3:
		circle(x, y, z, 2)	
		z -= 1
	G0(Z=sz)
	


def f():

	G0(0,0,sz)
	dep = -9
	#дырки

#	drill(14.5, 23, 0, dep, dep/2)
#	drill(14.5, 23 + 105, 0, dep, dep/2)
#	drill(14.5 + 105, 23, 0, dep, dep/2)
#	drill(14.5 + 105, 23 + 105, 0, dep, dep/2)

	G0(Z = sz)
	tr = 3.14/3
	z = 0
	while z > dep:
		for r in xrange(10, 60, 7):
			oval(67, 77, z, r, r, 0.2, tr*2 - 0.2)
			G0(Z = sz)
			oval(67, 77, z, r, r, tr*2 + 0.2, tr*4 - 0.2)
			G0(Z = sz)
			oval(67, 77, z, r, r, tr*4 + 0.2, tr*6 - 0.2)
			G0(Z = sz)
			
		z -= 1
	G0(Z = sz)

	#финальный прямоугольник
	G0(Z=sz)
	G0(0, 0)
	z = 0
	while z > dep:
		G1(Z=z)
		G1(X=133.7)
		G1(Y=153.7)
		G1(X=0)
		G1(Y=0)
		z -= 1
	
	G0(Z=5)


print("g21 g64 g90")
print("F400")
export(f)

