# -*- coding: utf-8 -*-

#Всякие вспомогательные функции
from main import *

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
	G0(Y = y + r)
	G1(Z=z)
	while a <= 6.3:
		G1(X = r*sin(a) + x, Y = r*cos(a) + y)
		a+=0.1

#написАл заранее
def cutLine(x1, y1, x2, y2, z1, z2, step):
	'прорезает щель с постепенным погружением'
	G1(X=x1, Y=y1, Z=z1)
	for z in xrange(z1, z2, step*2):
		G1(Z=z + step/2)
		G1(X=x2, Y=y2)
		G1(Z = z + step)
		G1(x1, y1)