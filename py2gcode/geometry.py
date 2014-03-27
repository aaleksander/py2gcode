#-*- coding: utf-8 -*-

from math import *

#вычислительная геометрия
#многое взято отсюда: http://hardfire.ru/all_geom
eps = 1e-8
pi = 3.14159265358979323

IN_CIRCLE 	= 0
ON_CIRCLE 	= 1
OUT_CIRCLE 	= 2

def to_point(dict):
    return Point(dict['x'], dict['y'])

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

def get_cross_point(p11, p12, p21, p22):
    'возвращает точку пересечения двух отрезков'
    # +0.0 делаем, чтобы преобразовать в double
    x1, y1 = p11.x + 0.0, p11.y + 0.0
    x2, y2 = p12.x + 0.0, p12.y + 0.0
    x3, y3 = p21.x + 0.0, p21.y + 0.0
    x4, y4 = p22.x + 0.0, p22.y + 0.0
    
    Z  = (y2-y1)*(x3-x4)-(y3-y4)*(x2-x1)
    Ca = (y2-y1)*(x3-x1)-(y3-y1)*(x2-x1)
    Cb = (y3-y1)*(x3-x4)-(y3-y4)*(x3-x1)

    #прямые совпадают
    if Z == 0 and Ca == 0 and Cb == 0:
        return None

    #прямые параллельны
    if Z == 0:
        return None

    Ua = Ca/Z
    Ub = Cb/Z

    return Point(x1 + (x2 - x1) * Ub, y1 + (y2 - y1) * Ub)
    
def is_cross(p11, p12, p21, p22):
    'возрващает True, если отрезки пересекаются'
    
    # +0.0 делаем, чтобы преобразовать в double
    x11, y11 = p11.x + 0.0, p11.y + 0.0
    x12, y12 = p12.x + 0.0, p12.y + 0.0
    x21, y21 = p21.x + 0.0, p21.y + 0.0
    x22, y22 = p22.x + 0.0, p22.y + 0.0    
    
    maxx1 = max(x11, x12)
    maxy1 = max(y11, y12)
    minx1 = min(x11, x12)
    miny1 = min(y11, y12)
    maxx2 = max(x21, x22)
    maxy2 = max(y21, y22)
    minx2 = min(x21, x22)
    miny2 = min(y21, y22)

    if minx1 > maxx2 or maxx1 < minx2 or miny1 > maxy2 or maxy1 < miny2:
        return False  # Момент, када линии имеют одну общую вершину...
 
    dx1, dy1 = x12-x11, y12-y11 # Длина проекций первой линии на ось x и y
    dx2, dy2 = x22-x21, y22-y21 # Длина проекций второй линии на ось x и y
    dxx, dyy = x11-x21, y11-y21;
    ddiv = dy2*dx1 - dx2*dy1
    
    mmul = dx1*dyy - dy1*dxx

    if ddiv == 0: #Линии параллельны...
        if x11 == x21 and x12 == x22 and y11 == y21 and y12 == y22:
            return True #совпадают 
        else:
            return False #не совпадают
    if ddiv > 0:
        mmul = dx1*dyy - dy1*dxx
        if mmul < 0 or mmul > ddiv:
            return False # Первый отрезок пересекается за своими границами...
        mmul = dx2*dyy - dy2*dxx
        if mmul < 0 or mmul > ddiv:
            return False # Второй отрезок пересекается за своими границами...
    
    mmul = -(dx1*dyy - dy1*dxx)
    if mmul < 0 or mmul > -ddiv:
        return False # Первый отрезок пересекается за своими границами...
    
    mmul = -(dx2*dyy - dy2*dxx)
    if mmul < 0 or mmul > -ddiv:
        return False # Второй отрезок пересекается за своими границами...

    return True

def get_border(p1, p2, w):
    'возвращает координаты прямоугольника, описанного вокруг отрезка'
    angle = get_angle(p1, Point(p1.x + 10, p1.y), p1, p2)
    r1 = Point(p1.x - w*sin(angle), p1.y + w*cos(angle))
    r2 = Point(p2.x - w*sin(angle), p2.y + w*cos(angle))
    r3 = Point(p2.x + w*sin(angle), p2.y - w*cos(angle))
    r4 = Point(p1.x + w*sin(angle), p1.y - w*cos(angle))
    return (r1, r2, r3, r4)

import unittest

class TestCliper(unittest.TestCase):    
    def test_is_cross(self):
        p1 = Point(0, 0)
        p2 = Point(10, 10)
        p3 = Point(0, 10)
        p4 = Point(10, 0)
        self.assertTrue(is_cross(p1, p2, p3, p4), "Неправильно определил факт пересечения")        
        p = get_cross_point(p1, p2, p3, p4)
        self.assertTrue(p.x == 5.0, 'неверно определи координату Х пересечения')
        self.assertTrue(p.y == 5.0, 'неверно определи координату Y пересечения')
        
    def test_vertex_on_line(self):
        p1, p2 = Point(0, 0), Point(20, 0)
        p3, p4 = Point(10, 10), Point(10, 0) #эта линия лежит одной вершиной на p1, p2

        self.assertTrue(is_cross(p1, p2, p3, p4), 'неверно определил факт пересечения')
        p = get_cross_point(p1, p2, p3, p4)
        self.assertTrue(p.x == 10.0, 'неверно Х')
        self.assertTrue(p.y == 0.0, 'неверно Y')
        
    def test_sovpadaut(self):
        p1, p2 = Point(0, 0), Point(10, 10)
        p3, p4 = Point(0, 0), Point(10, 10)
        p5, p6 = Point(0, 10), Point(10, 20) #параллельна p1-p2
        self.assertTrue(is_cross(p1, p2, p3, p4))
        self.assertFalse(is_cross(p1, p2, p5, p6)) #параллельные
        self.assertTrue(get_cross_point(p1, p2, p3, p4) == None)

if __name__ == '__main__':
    unittest.main()
