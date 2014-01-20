# -*- coding: utf-8 -*-

#вырезает за один раз коробочку с крышкой

from py2gcode import *

#внутренние размеры в мм
in_width = 30.0
in_length = 50.0
#глубина низа
dep_1 = 15.0
#глубина крышки
dep_2 = 15.0
#толщина материала
thickness = 20.0
#толщина стенки
wall = 10.0
#диаметр инструмента
diam = 3.0

safeZ=5

def UP():
	#поднимает фрезу на безопасное расстояние
	G0(Z = safeZ)

def fill_rect_pref(x, y):
	G0(Z = safeZ)
	G0(x + diam/2, y + diam/2)

def fill_rect(x, y, length, width, w=None):
	#w - толщина границы, None - если надо вырезать всю площадь, либо - конкретную ширину пропила
	step = diam*0.7
	G0(x + diam/2, y + diam/2)

	#G1(Z = z)
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
		xl = x + w - diam/2
		xr = x + length - w + diam/2
		yt = y + width - w + diam/2
		yb = y + w - diam/2
		G1(xl, yb)
		G1(Y = yt)
		G1(X = xr)
		G1(Y=yb)
		G1(X = xl)
	G0(Z = safeZ)

def cut_rect(x, y, length, width, depth):
	#вырезаем прямоугольник определенного размера на определенную глубину
	#с перемычками
	G0(Z=safeZ)
	#обрезаем коробочку
	z = -diam
	G0(x - diam/2, y - diam/2)
	while z > depth - 1:
		G1(Z = z)
		G1(Y = y + width + diam/2)
		G1(X = x + length  + diam/2)
		G1(Y = y - diam/2)
		G1(x - diam/2)
		z -= diam
	G0(Z = safeZ)
	#Последний проход, с перемычками
	z = -thickness - 1
	G0(x - diam/2, y - diam/2)
	G1(Z = z)	
	G1(Y = y + width/2 - 5 + diam/2 )
	G0(Z = depth + 1)
	G1(Y = y + width/2 + 5 + diam/2 )
	G1(Z = z)	
	G1(Y = y + width + diam/2 )

	G1(X = x + length + diam/2)

	G1(Y = y + width/2 + 5 + diam/2 )
	G0(Z = depth + 1)
	G1(Y = y + width/2 - 5 + diam/2 )
	G1(Z = z)	
	G1(Y = y - diam/2 )
	G1(x - diam/2)

def f():
	G0(0, 0, 0)

#вырезаем низ
	#основное углубление
	immersion(0, -dep_1, diam, 
		lambda: fill_rect_pref(0, 0), 
		lambda: fill_rect(0, 0, in_length, in_width))

	immersion(0, -thickness/2, diam,
		lambda: fill_rect_pref(-wall, -wall), 
		lambda: fill_rect(-wall, -wall, in_length + 2*wall, in_width + 2*wall, wall/2))

	cut_rect(-wall, -wall, in_length + 2*wall, in_width + 2*wall, -thickness)

#пошла вторая часть
	off_x = in_length + wall*2 + diam

	immersion(0, -thickness/2, diam, 
		lambda: fill_rect_pref(0 + off_x - wall/2, -wall/2), 
		lambda: fill_rect(-wall/2 + off_x, -wall/2, in_length + wall, in_width + wall))

	immersion(-thickness/2, -dep_2, diam, 
		lambda: fill_rect_pref(0 + off_x, 0), 
		lambda: fill_rect(0 + off_x, 0, in_length, in_width))

	cut_rect(-wall + off_x, -wall, in_length + 2*wall, in_width + 2*wall, -thickness)

print("g21 g64 g90")
print("F1200")
preview(f)
#export(f)


