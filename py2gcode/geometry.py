# -*- coding: utf-8 -*-

from math import sqrt

#всякие геометрические штуки
#взято отсюда: http://hardfire.ru/all_geom
eps = 1e-8;
pi = 3.14159265358979323;

IN_CIRCLE 	= 0
ON_CIRCLE 	= 1
OUT_CIRCLE 	= 2


class Point:
	def __init__(self, x, y):
		self.x = x;
		self.y = y

class Circle:
	def __init__(self, x, y, r):
		self.c = Point(x, y)
		self.r = r

class Line:
	def __init__(self, a, b, c):
		self.a = a
		self.b = b
		self.c = c

def contact_points (p, c):
	'''точки касания касательной с окружностью
		возвращает кортеж точек (обычно двух)
		p - Point
		c - Circle
	'''
	flag = point_in_circle (p, c)
	
	if flag == IN_CIRCLE: 
		return ()
	if flag == ON_CIRCLE:        
		return (p)
    
    #находим расстояние до точек касания
	d = dist (p, c.c)
	k = sqrt (d * d - c.r * c.r)
	return cross_circle(p.x, p.y, k, c.c.x, c.c.y, c.r)

def dist(a, b):
	'расстояние между двумя точками'
	return sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y))


def point_in_circle (p, c):
	'''положение точки относительно окружности
		p - Point
		c - Circle
	'''
	d = dist (p, c.c)
	if abs (c.r - d) <= eps:
		return ON_CIRCLE #на окружности
	
	if c.r > d: #за пределами окружности	
		return IN_CIRCLE
	
	return OUT_CIRCLE#внутри окружности


def cross_circle (x1, y1, r1, x2, y2, r2):
	'''пересечение окружностей
		возвращает кортеж Point
	'''
	if  abs (x1 - x2) <= eps and abs (y1 - y2) <= eps and abs (r1 - r2) <= eps:
		return () #окружности совпадают
	a = 2.0 * (x2 - x1)
	b = 2.0 * (y2 - y1)
	c = x1 * x1 + y1 * y1 - r1 * r1 - (x2 * x2 + y2 * y2 - r2 * r2)
	return cross_line_circle (Line (a, b, c), Circle (x1, y1, r1))

def cross_line_circle (l, c):
	'''пересечение прямой с окружностью
		l - Line
		c - Circle
		return кортеж Point'''
    #проекция центра окружности на прямую
	p = closest_point (l, c.c)
    #сколько всего решений?
	flag = 0
	d = dist (c.c, p)
	if abs (d - c.r) <= eps: 
		flag = 1
	else:
		if c.r > d: 
			flag = 2
		else:
			return ()

    #находим расстояние от проекции до точек пересечения
	k = sqrt (c.r * c.r - d * d)
	t = dist (Point(0, 0), Point (l.b, - l.a))
	#добавляем к проекции векторы направленные к точкам пеерсечения
	p1 = add_vector (p, Point (0, 0), Point (- l.b, l.a), k / t);
	p2 = add_vector (p, Point (0, 0), Point (l.b, - l.a), k / t);
	return (p1, p2)


def closest_point (l, p):
	'''проекция точки на прямую'''
	k = (l.a * p.x + l.b * p.y + l.c) / (l.a * l.a + l.b * l.b)
	return Point (p.x - l.a * k, p.y - l.b * k)



def add_vector (p, p1, p2, k):
	'''добавление заданной части вектора к точке'''
	return Point (p.x + (p2.x - p1.x) * k, p.y + (p2.y - p1.y) * k);
