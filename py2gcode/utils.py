# -*- coding: utf-8 -*-

#Всякие вспомогательные функции
from main import *

def rect(x, y, w, h, z):
	'''
	обводит треугольник на глубине z
	x, y - координата
	w, h - ширина и длина
	'''
	G1(Z = z)
	G1(X = x + w)
	G1(Y = y + h)
	G1(X = x)
	G1(Y = y)



def circle(x, y, r):
	'''
	x, y - координаты центра
	'''
	