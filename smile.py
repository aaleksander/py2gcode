# -*- coding: utf-8 -*-


from py2gcode import *

sz = 2

def f():
	G0(0, 0)

	z = -1
	G1(Z=-1)
	G1(0, 30)
	G1(20)
	G1(Y=0)

	G0(Z=sz)
	G0(30, 0)
	G1(Z=-1)
	G1(40, 30)
	G1(50, 0)

	G0(Z=sz)
	G0(35, 10)

	G1(Z=-1)
	G1(X=45)

	G0(Z=sz)
	G0(60, 30)
	G1(Z=-1)
	G1(Y=0)
	G1(X=80)
	G1(Y=30)

	G0(Z=sz)
	G0(70, 20)
	G1(Z=-1)
	G1(Y=0)

	G0(Z=sz)
	G0(90, 0)
	G1(Z=-1)
	G1(100, 30)
	G1(110, 0)

	G0(Z=sz)
	G0(95, 10)

	G1(Z=-1)
	G1(X=105)



#	while z > -20:
#		oval(50, 70, z, 3, 5)
#		G0(Z=sz)
#		oval(70, 70, z, 3, 5)
#		G0(Z=sz)

#		oval(60, 68, z, 20, 20, 3.14 + 0.3, 6.28-0.3)
#		G0(Z=sz)
	
#		oval(60, 68, z, 20, 25, 3.14 + 0.25, 6.28-0.25)
#		G0(Z=sz)

#		circle(60, 60, z, 25)
#		G0(Z=sz)
#		z -= 1

print("g21 g64 g90")
print("F300")
export(f)
