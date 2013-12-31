# -*- coding: utf-8 -*-

#решетка на системник

from py2gcode import *


def elem_lb(x, y, z, sz, s):
	'''вырезаем один элемент
	s - "размер""
	sz - безопасная высота
	'''
	#левый-нижний уголок
	G1(x + s)
	G1(Y = y + s)
	G1(x + s + s)
	G1(Y = y + s + s)
	G1(x)
	G1(Y=y)

def elem_rb(x, y, z, sz, s):
	#правый нижний
	print "lb"
	G0(x, y + s)
	G1(Z=z)
	G1(x + s)
	G1(Y = y)
	G1(x + s*2)
	G1(Y = y + s*2)
	G1(x)
	G1(Y = y + s)
	G0(Z = sz)

def elem_lt(x, y, z, sz, s):
	'левый верхний'
	G0(x, y)
	G1(Z = z)
	G1(x + s*2)
	G1(Y = y + s)
	G1(x + s)
	G1(Y = y + s*2)
	G1(x)
	G1(Y = y)
	G0(Z = sz)

def elem_rt(x, y, z, sz, s):
	'правый верхний'
	G0(x, y)
	G1(Z = z)
	G1(x + s*2)
	G1(Y = y + s*2)
	G1(x + s)
	G1(Y = y + s)
	G1(x)
	G1(Y = y)
	G1(Z = sz)

def cent(x, y, z, sz, s):
	'центральное отверстие'
	G0(x, y)
	G1(Z = z)
	G1(X = x + s)
	G1(Y = y + s)
	G1(X = x)
	G1(Y = y)
	G0(Z = sz)


def f():
	clearCNC()
	G0(0, 0, 0)

	for x in xrange(0, 30, 30):
		immersion(0, 10, 5, lambda: elem_lb(x 	   ,   0, 5))
		G0(Z = 10)

		#elem_lb(x 	   ,   0, 10, 0,  5)
		#elem_rb(x + 15 ,   0, 10, 0,  5)
		#elem_lt(x      , -15, 10, 0,  5)
		#elem_rt(x + 15 , -15, 10, 0,  5)
		#cent   (x + 10,   -5, 10, 0, 5)


preview(f)
export(f, "d")