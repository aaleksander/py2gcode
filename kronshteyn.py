# -*- coding: utf-8 -*-

#Кронштейн для гровера. Шейка = 50 мм

from py2gcode import *

sz = 5
def f():
	G0(X=0, Y=0, Z=0)

	z = -7.5 #начальная глубина

	#штрихи под свершелку
#	G0(X=20)
#	G1(Z=z)
#	G1(Y=40)
#	G0(Z=sz)

#	G0(X=130)
#	G1(Z=z)
#	G1(Y=0)
#	G0(Z=sz)

#	G0(X=60, Y=90)
#	G1(Z=z)
#	G1(X=90)
#	G0(Z=sz)
	while z > -20:
		G0(Z=sz)	
		circle(75, 40, z, 23.5)
		G0(Z=sz)

		G0(75, 105)
		G1(Z = z)
		G1(X = 90)
		G1(Y=82.5)

		oval(75, 40, z, 45, 45, 3.14/2 - 0.340, 0)
		G1(X=75+45+30)
		G1(Y=0)
		G1(X=0)
		G1(Y=40)
		G1(X=30)
		oval(75, 40, z, 45, 45, 3.14, 3.14/2 + 0.34)
		G1(Y=105)
		G1(X=75)
		G1(Y=65)
		z -= 1	

	G0(Z=sz)
	G0(X=0, Y=0)

print("g21 g64 g90")
print("F400")
#export(f)
preview(f)
