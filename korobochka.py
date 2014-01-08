# -*- coding: utf-8 -*-

#вырезает за один раз коробочку с крышкой

from py2gcode import *

#безопасная высота
sz = 5
#внутренние размеры в мм
in_width = 30.0
in_length = 50.0
#глубина низа
dep_1 = 10.0
#глубина крышки
dep_2 = 0.0
#толщина материала
tol = 20.0
#диаметр инструмента
diam = 3.0

def UP():
	#поднимает фрезу на безопасное расстояние
	G0(Z = sz)

def fill_rect(x, y, length, width, z, w=None):
	#w - толщина границы, None - если надо вырезать всю площадь
	step = diam*0.7
	G0(Z = sz)
	G0(x + diam/2, y + diam/2)
	
	G1(Z = z)
	xl = x + diam/2
	xr = x + length - diam/2
	yt = y + width - diam/2
	yb = y + diam/2
	
	if w == None:
		while xr >= xl and yt >= yb:
			G1(xl, yb)
			G1(Y = yt)
			G1(X = xr)
			G1(Y=yb)
			G1(X = xl)

			yb += step
			xr -= step
			yt -= step
			xl += step

	else:
		ww = diam
		while ww <= w:
			G1(xl, yb)
			G1(Y = yt)
			G1(X = xr)
			G1(Y=yb)
			G1(X = xl)

			yb += step
			xr -= step
			yt -= step
			xl += step
			ww += step

		#завершающий круг, чтобы выровнять размеры
		ww = w - diam
		G1(x + diam/2 + ww, y + diam/2 + ww)
		G1(Y = width - ww - diam/2)
		G1(X = length - ww - diam/2)
		G1(Y = y + diam/2 + ww)
		G1(X = x + diam/2 + ww)
	G0(Z = sz)
	

def f():
	G0(Z=sz)
	G0(0, 0)


	#вырезаем низ
	z = -diam

	while z > -dep_1:
		fill_rect(0, 0, in_length, in_width, z)
		z -= diam
	#если не достигли заданной глубины
	if z != -dep_1:
		fill_rect(0, 0, in_length, in_width, -dep_1)
	G0(Z = sz)

	#бортик	
	z = -diam
	while z > -(tol/2):
		fill_rect(-10, -10, in_length + 20, in_width + 20, z, 5)
		z -= diam
	#если не достигли заданной глубины
#	if z != -(tol/2):
#		fill_rect(-10, -10, in_length + 20, in_width + 20, -(tol/2), 5)
	G0(Z = sz)

	'''
	G0(Z=sz)
	#обрезаем коробочку
	z = -diam
	G0(-10 - diam/2, -10 - diam/2)
	while z > -tol + 1:
		G1(Z = z)
		G1(Y = in_length + 10 + d/2)
		G1(X = in_width + 10 + d/2)
		G1(Y = -10 - d/2)
		G1(-10 - d/2)
		z -= d
	G0(Z = sz)
	#Последний проход, с перемычками
	z = -tol - 1
	G0(-10 - d/2, -10 - d/2)
	G1(Z = z)	
	G1(Y = in_length/2 - 5 + d/2 )
	G0(Z = -tol + 1)
	G1(Y = in_length/2 + 5 + d/2 )
	G1(Z = z)	
	G1(Y = in_length + 10 + d/2 )

	G1(X = in_width + 10 + d/2)


	G1(Y = in_length/2 + 5 + d/2 )
	G0(Z = -tol + 1)
	G1(Y = in_length/2 - 5 + d/2 )
	G1(Z = z)	
	G1(Y = -10 - d/2 )
	G1(-10 - d/2)
	'''
	G0(Z=sz)
	G0(0, 0)

#пошла вторая часть
	'''
	z = -d
	off_x = 0#in_width + 20 + d

	#основное углубление
	while z > -dep_2:
		fill_rect(d/2 + off_x, in_length - d/2, in_width - d/2 + off_x, 0 + d/2, z, d*0.7)
		z -= d
	#если не достигли заданной глубины
	if z != -dep_2:
		fill_rect(d/2 + off_x, in_length - d/2, in_width - d/2 + off_x, d/2, -dep_2, d*0.7)
	G0(Z = sz)

	#бортик "наоборoт", т.е. ответная часть
	z = -d
	while z > -(tol/2):
		w = d*0.35
		G0(off_x - w, w)
		while w <= 5 + d/2:
			G1(-w + off_x, -w)
			G1(Z = z)
			G1(Y = w + in_length)
			G1(X = w + in_width + off_x)
			G1(Y= -w)
			G1(-w + off_x)
			w += d*0.7

		if w > 5 - d/2:
			w = 5 - d/2
			G1(-w + off_x, -w)
			G1(Z = z)
			G1(Y = w + in_length)
			G1(X = w + in_width + off_x)
			G1(Y= -w)
			G1(-w + off_x)
		G0(Z=sz)

		z -= d

	#обрезаем коробочку

	z = -d
	G0(-10 - d/2 + off_x, -10 - d/2)
	while z > -tol + 1:
		G1(Z = z)
		G1(Y = in_length + 10 + d/2)
		G1(X = in_width + 10 + d/2 + off_x)
		G1(Y = -10 - d/2)
		G1(-10 - d/2 + off_x)
		z -= d
	G0(Z = sz)
	#Последний проход, с перемычками
	z = -tol - 1
	G0(-10 - d/2 + off_x, -10 - d/2)
	G1(Z = z)	
	G1(Y = in_length/2 - 5 + d/2 )
	G0(Z = -tol + 1)
	G1(Y = in_length/2 + 5 + d/2 )
	G1(Z = z)	
	G1(Y = in_length + 10 + d/2 )

	G1(X = in_width + 10 + d/2 + off_x)


	G1(Y = in_length/2 + 5 + d/2 )
	G0(Z = -tol + 1)
	G1(Y = in_length/2 - 5 + d/2 )
	G1(Z = z)	
	G1(Y = -10 - d/2 )
	G1(-10 - d/2 + off_x)

	G0(Z=sz)
	G0(0, 0)
	'''
	
	



print("g21 g64 g90")
print("F1200")
export(f)


