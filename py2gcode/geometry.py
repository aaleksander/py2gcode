# -*- coding: utf-8 -*-

from math import *

#вычислительная геометрия
#многое взято отсюда: http://hardfire.ru/all_geom
eps = 1e-8;
pi = 3.14159265358979323;

IN_CIRCLE 	= 0
ON_CIRCLE 	= 1
OUT_CIRCLE 	= 2


class Point:
	def __init__(self, x, y):
		self.x = x;
		self.y = y
		self.tag = None

	def __eq__(self, other):
		if isinstance(other, Point) == False:
			return False
		return other.x == self.x and other.y == self.y

	def copy(self):
		return Point(self.x, self.y)

	def __str__(self):
		return "Point(%(x)s, %(y)s)" % {'x': self.x, 'y': self.y}

	def __sub__(self, b):
		return Point(self.x - b.x, self.y - b.y)

class Circle:
	def __init__(self, x, y, r):
		self.c = Point(x, y)
		self.r = r

	def __str__(self):
		return "Circle(%(x)s, %(y)s, %(r)s)" % {'x': self.c.x, 'y': self.c.y, 'r': self.r}


class Line:
	def __init__(self, a=None, b=None, c=None, p1=None, p2=None):
		if p1 == None:
			self.a = a
			self.b = b
			self.c = c
		if p2 != None and p1 != None:
			self.p1 = p1
			self.p2 = p2
			self.a = p2.y - p1.y
			self.b = p1.x - p2.x
			self.c = -self.a*p1.x - self.b*p1.y

	def __str__(self):
		return "Line(%(a)s, %(b)s, %(c)s)" % {'a': self.a, 'b': self.b, 'c': self.c}


	def init_p1(self, x):
		'вычисляем одну точку по какой-нибудь координате'
		self.p1 = Point(x, (-self.a*x - self.c)/self.b)

	def init_p2(self, x):
		'вычисляем одну точку по какой-нибудь координате'
		self.p2 = Point(x, (-self.a*x - self.c)/self.b)


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

def contact_lines(c1, c2):
	'''Возвращает массив всех общих касательных двух окружностей'''
	def tangents (c, r1, r2):
		'вовзращает одну линию r1, r2 - радиусы, с - какая-то точка'
		r = r2 - r1;
		z = c.x*c.x + c.y*c.y;
		d = z - r*r;
		if (d < -eps):
			return None
		d = sqrt (abs (d));
		
		a = (c.x * r + c.y * d) / z;
		b = (c.y * r - c.x * d) / z;
		c = r1;
		return Line(a, b, c)

	res = []
	for i in xrange(-1, 2, 2):
		for j in xrange(-1, 2, 2):
			l = tangents (c2.c - c1.c, c1.r*i, c2.r*j)
			if l != None:
				res.append(l)
	for l in res:
		l.c -= (l.a * c1.c.x + l.b * c1.c.y);

	#теперь найдем точки пересечения этих касательных с окружностями
	for l in res:
		pp = cross_line_circle(l, c1)
		l.p1 = pp[0]
		pp = cross_line_circle(l, c2)
		l.p2 = pp[0]
	return res


def dist(a, b):
	'расстояние между двумя точками, теорема Пифагора'
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
	if abs (d - abs(c.r)) <= eps: 
		flag = 1
	else:
		if c.r > d: 
			flag = 2
		else:
			print "облом"
			return ()

    #находим расстояние от проекции до точек пересечения
	if flag == 1:
		k = 0
	else:
		k = sqrt (c.r * c.r - d * d)

	t = dist (Point(0, 0), Point (l.b, - l.a))
	#добавляем к проекции векторы направленные к точкам пересечения
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

def get_angle(p11, p12, p21, p22):
	'возвращает угол между двумя отрезками'
	l1 = sqrt((p11.x - p12.x)*(p11.x - p12.x) + (p11.y - p12.y)*(p11.y - p12.y))
	l2 = sqrt((p21.x - p22.x)*(p21.x - p22.x) + (p21.y - p22.y)*(p21.y - p22.y))

	v1 = Point(0, 0)
	v2 = Point(0, 0)
	v1.x = (p12.x/l1 - p11.x/l1);
	v1.y = (p12.y/l1 - p11.y/l1);
	v2.x = (p22.x/l2 - p21.x/l2);
	v2.y = (p22.y/l2 - p21.y/l2);


  	res = atan2(v1.x*v2.y - v2.x*v1.y, v1.x*v2.x + v1.y*v2.y)

	if res < 0:
		res = pi + (pi - abs(res))

	return res


