# -*- coding: utf-8 -*-

#Всякие вспомогательные функции
from main import *

safeZ = 5

def rect_pref(x, y):
	G0(Z=safeZ)
	G0(x, y)

def rect(x, y, w, h, z):
	'''
	обводит прямогольник на глубине z
	x, y - координата
	w, h - ширина и длина
	'''
	G1(Z = z)
	G1(X = x + w)
	G1(Y = y + h)
	G1(X = x)
	G1(Y = y)

def circle(x, y, z, r):
	'''
	x, y - координаты центра
	'''
	a = 0
	G0(X = r*sin(a) + x, Y = r*cos(a) + y)
	G1(Z=z)
	while a <= 6.3:
		G1(X = r*sin(a) + x, Y = r*cos(a) + y)
		a+=0.1

def oval(x, y, z, rx, ry, aStart=0, aStop=6.3):
	'''
	почти тоже самое, что и круг, только с двумя разными радиусами
	x, y - координаты центра
	'''
	a = aStart
	G0(X = rx*cos(a) + x, Y = ry*sin(a) + y)
	G1(Z=z)
	if aStart<aStop:
		while a <= aStop:
			G1(X = rx*cos(a) + x, Y = ry*sin(a) + y)
			a+=0.1
	else:
		while a >= aStop:
			G1(X = rx*cos(a) + x, Y = ry*sin(a) + y)
			a-=0.1
	

#написАл заранее
def cutLine(x1, y1, x2, y2, z1, z2, step):
	'прорезает щель с постепенным погружением'
	G1(X=x1, Y=y1, Z=z1)
	for z in xrange(z1, z2, step*2):
		G1(Z=z + step/2)
		G1(X=x2, Y=y2)
		G1(Z = z + step)
		G1(x1, y1)


def immersion(z1, z2, step, pref, f):
	'''f - это подпрограмма *горизонтальной* обработки
	программа выполняет эту подпрограмму, погружаясь с глубины z1 до z2 с шагом	
	ПОДПРОГРАММА ДОЛЖНА БЫТЬ ЦИКЛИЧНА
	z1 должен быть больше z2 (z1 - верх, z2 - низ)
	'''
	G0(Z=safeZ)
	z = z1	
	while z>z2:
		pref()
		G1(Z = z)
		f()
		z -= step
		G0(Z=safeZ)
	if z != z2:
		pref()
		G1(Z=z2)
		f()
	G0(Z=safeZ)


