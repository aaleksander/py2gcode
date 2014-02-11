# -*- coding: utf-8 -*-
from Tkinter import *
from geometry import *
from math import cos, sin
from main import *
from trajectory import *

#построение мета-траекторий, т.е. замкнутых траекторий на основе каких-то опорных точек и с помощью "эластичной ленты" вокруг всех точек
'''
опорная точка - это словарь со следующими полями
x, y - координата
radius - радиус точки, по умолчанию - ноль
	- если радиус отрицательный, то траектория его "обойдет" с другой стороны
rouonding - скругление угла с заданным радиусом, всегда положительно
'''

def get_from_ring(l, i, off):
    'возвращает сегмент из массива l как будто это кольцевой список, i-позиция, off - смещение относительно этой позиции'
    o = i + off
    if o >= len(l):
        while o >= len(l):
            o -= len(l)
    else:
        if o < 0:
            while i<0:
                o += len(l)
    return l[o]

#типы сегментов
SEG_LINE	= 1 #прямая лини
SEG_ARC 	= 2 #дуга
SEG_ROUND	= 3 #дуга на углу
class Segment:
    '''
        Один сегмент траетории
    '''
    def __init__(self, type, p1, p2, center = None, radius = None):
        'создает сегмент типа дуга, p1, p2 - начало конец, p3 - центр'
        self.type = type
        self.p1 = p1.copy()
        self.p2 = p2.copy()
        self.center = None
        if center != None:
            self.center = center.copy()
        self.radius = None
        if radius != None:
            self.radius = radius

    def draw(self, canvas, color):
        'рисуем сегмент на канве'
        pass

    def __str__(self):
        return "%(t)s, %(p1)s, %(p2)s, %(c)s, %(r)s" % {'t': self.type, 'p1': self.p1, 'p2': self.p2, 'c': self.center, 'r': self.radius}

    def get_lines(self, canvas=None):
        '''возвращает список координат, готовый для рисования на канве
        т.е. просто список: x, y, x, y, x, y, x, y, x, y ...		'''

        def get_line_for_arc(p1, center, p2,  dir = False):
            '''считает линии для дуги от точки до точки и с центром
            dir == False - против часовой
            '''
            #считаем начальный угол
            zero = Point(center.x + 100, center.y)
            a1 = get_angle(center, p1, center, zero)
            a2 = get_angle(center, p2, center, zero)

            if self.radius < 0:
                a1, a2 = a2, a1

            if a1 < a2:
                a1 += 2*pi

            r = dist(center, p1)
            res = []
            if dir:
                while a1 > a2:
                    res.append(center.x + r*cos(a1))
                    res.append(center.y - r*sin(a1))
                    a1 = a1 - 0.1
                #последний шажок, если в цикле "перебежали"
                if a1 < a2:
                    res.append(center.x + r*cos(a2))
                    res.append(center.y - r*sin(a2))
            else:        
                while a1 > a2:
                    res.append(center.x + r*cos(a2))
                    res.append(center.y - r*sin(a2))
                    a2 = a2 + 0.1
                #последний шажок, если в цикле "перебежали"
                if a1 < a2:
                    res.append(center.x + r*cos(a1))
                    res.append(center.y - r*sin(a1))
            
            return res

        if self.type == SEG_ARC: #скругляем дугу относительно центра
            res = get_line_for_arc(self.p1, self.center, self.p2,  self.radius > 0)
        else: #простое скругление угла
            p1,  cr,  p2,  dir = self.round(self.p1,  self.center,  self.p2,  self.radius)

            if dir == True:
                res = get_line_for_arc(p1, cr, p2,  dir)
            else:
                res = get_line_for_arc(p2, cr, p1,  dir)
        return res

    def round(self, p1, c, p2, r):
        '''      Скругляет угол с заданым радиусом
                Получает на вход p1, center, p2, radius
                возвращает [p1, center, p2], готовое для скармливания get_line_for_arc '''        
        a1 = get_angle(p1, c, p1, Point(p1.x + 100, p1.y))
        a2 = get_angle(p1, c, c, p2)
        rr1 = self.__get_border(p1, c, r)
        rr2 = self.__get_border(c, p2, r)

        if a2 > pi:
            cr = get_cross_point(rr1[2], rr1[3], rr2[2], rr2[3])
            dir = True
        else:
            cr = get_cross_point(rr1[0], rr1[1], rr2[0], rr2[1])
            dir = False

        pp = contact_points(c, Circle(cr.x, cr.y, r))

        if dir:
            return (pp[0],  cr,  pp[1],  dir)
        else:
            return (pp[1],  cr,  pp[0],  dir)

    def __get_border(self, p1, p2, w):
        'возвращает координаты прямоугольника, описанного вокруг отрезка'
        angle = get_angle(p1, Point(p1.x + 10, p1.y), p1, p2)
        r1 = Point(p1.x - w*sin(angle), p1.y + w*cos(angle))
        r2 = Point(p2.x - w*sin(angle), p2.y + w*cos(angle))
        r3 = Point(p2.x + w*sin(angle), p2.y - w*cos(angle))
        r4 = Point(p1.x + w*sin(angle), p1.y - w*cos(angle))
        return (r1, r2, r3, r4)

    def to_gcode(self):
        ll = self.to_points()
        for l in ll:
            G1(l['x'],  l['y'])
            
    def to_points(self):
        'разбить на отдельные точки для траектории'
        ll = self.get_lines()
        pair = lambda arr: [arr[i:i + 2] for i in range(0, len(arr), 2)]	#разбивает на пары

        ll = pair(ll)
        res = []
        for l in ll:        
            res.append({'x': l[0],  'y':l[1]})
            
        return res


class Meta(Trajectory):
    'Метатраектория'
    def __init__(self):
        super(Meta,  self).__init__()
        
        self.refPoints = [] #опорные точки

    def point(self, x, y, radius=None, rounding=None):
        self.refPoints.append( point(x, y, radius, rounding))

    def draw_points(self, canvas,  scr_x,  scr_y,  scale):
        'рисуем сцену с учетом всех вращений, преобразований и сдвигов'
        #рисуем все точки в виде желтых окружностей с перекрестием
        for p in self.refPoints:
            x = p['x']*scale + scr_x
            y = p['y']*scale + scr_y
            self.__drawPoint(canvas,  x, y,  scale)
            if 'radius' in p.keys():
                r = p['radius'] * scale
                canvas.create_oval(x - r,  y - r, x + r, y + r, outline='yellow')

        #рисуем путь
        '''
        for s in self.path:
            if s.type == SEG_LINE:
                self.canvas.create_line(s.p1.x*scale, s.p1.y*scale, s.p2.x*scale, s.p2.y*scale, fill='red',  width=2)
            if s.type == SEG_ARC:
                self.canvas.create_line(map(lambda x: x*scale, s.get_lines()), fill='red',  width=2)#, arrow = LAST, arrowshape = (15, 20, 5))
            if s.type == SEG_ROUND:
                self.canvas.create_line(map(lambda x: x*scale, s.get_lines(self.canvas)), fill='red',  width=2)#, arrow = LAST, arrowshape = (15, 20, 5))

        return self.canvas #на тот случай, если кто-то еще захочет порисовать
        '''

    def __drawPoint(self, canvas,  x, y,  size):
        canvas.create_line(x, y - size, x, y + size, fill='yellow')
        canvas.create_line(x - size, y, x + size, y, fill='yellow')

    def create_trajectory(self):
        self.points = []
        self.create_path()
        first = True
        for s in self.path:
            #if first:
            #    self.points.append(point(s.p1.x,  s.p1.y))
            if s.type == SEG_LINE:
                if first:
                    self.points.append( point(s.p1.x,  s.p1.y))  #{'x': s.p2.x,  'y':s.p2.y})
                self.points.append( point(s.p2.x,  s.p2.y))  #{'x': s.p2.x,  'y':s.p2.y})
            if s.type == SEG_ARC:
                self.points += s.to_points()
                self.points.append(point (s.p2.x,  s.p2.y))# {'x': s.p2.x,  'y':s.p2.y})
            if s.type == SEG_ROUND:
                self.points += s.to_points()
                
            first = False

        self.update_offsets()

    def create_path(self):
        'создает траекторию по self.refPoints'
        self.path = []

        prev = self.refPoints[0]
        prevO = None#Point(None, None)
        first = True
        for p in self.refPoints[1:]:
            pp = self.__get_segment(prev, p) #расчитываем сегмент
            
            if len(pp) == 2:
                if isRound(prev) and first == True: #первая точка - скругление
                    self.path.append(Segment(SEG_ROUND, prev, prev, Point(prev['x'], prev['y']), prev['round']))

                if isCircle(prev) and first == False:#если предыдущая точка была окружность, то вставляем дугу
                    self.path.append(Segment(SEG_ARC, prevO, pp[0], Point(prev['x'], prev['y']), prev['radius']))

                if isRound(prev) and first == False:#скругляем угол
                    self.path.append(Segment(SEG_ROUND, p, p, prevO, prev['round']))

                self.path.append(Segment(SEG_LINE, pp[0], pp[1]))
                prevO = pp[1].copy()

            prev = p.copy() #запоминаем предыдущую точку
            first = False

        #завершаем контур
        pp = self.__get_segment(prev, self.refPoints[0])

        if isCircle(prev):#если предыдущая точка была окружность, то вставляем дугу
            self.path.append(Segment(SEG_ARC, prevO, pp[0], Point(prev['x'], prev['y']), prev['radius']))

        if isRound(prev):#скругляем угол
            self.path.append(Segment(SEG_ROUND, p, p, prevO, prev['round']))

        self.path.append(Segment(SEG_LINE, pp[0], pp[1]))

        if isCircle(self.refPoints[0]):			
            self.path.append(Segment(SEG_ARC, pp[1], self.path[0].p1, Point(self.refPoints[0]['x'], self.refPoints[0]['y']), self.refPoints[0]['radius']))

        #проходим по траектории и скругляем углы (round)
        new_path = []
        for i in xrange(0, len(self.path)):
            s = self.path[i]
            if s.type == SEG_ROUND:
                s_prev = get_from_ring(self.path, i, -1)
                s_past = get_from_ring(self.path, i, 1)
                p1, c, p2,  dir = s.round(s_prev.p1, s.center, s_past.p2, s.radius) #скругляем
                s.p1 = p1
                s.p2 = p2
                s_prev.p2 = p2
                s_past.p1 = p1                


    def __get_segment(self, p1, p2, p3=None):
        '''return кортеж Point'''
        if p1 == None or len(p1) == 0:
            return ()

        o1 = dict2object(p1)
        o2 = dict2object(p2)

        if isinstance(o1, Point) and isinstance(o2, Circle):
            pp = contact_points(o1, o2)
            if o2.r < 0:
                return (o1, pp[0])
            else:			
                return (o1, pp[1])

        if isinstance(o1, Circle) and isinstance(o2, Point):			
            pp = contact_points(o2, o1)
            if o1.r < 0:
                return (pp[1], o2)
            else:
                return (pp[0], o2)

        if isinstance(o1, Circle) and isinstance(o2, Circle):	
            ll = contact_lines(o1, o2)
            return (ll[0].p1, ll[0].p2)

        return (Point(p1['x'], p1['y']), Point(p2['x'], p2['y']))

def dict2object(o):
    'преобразует словарик в точку или окружность'
    if isCircle(o):
        return Circle(o['x'], o['y'], o['radius'])
    return Point(o['x'], o['y'])

def isCircle(p):
    return 'radius' in p.keys()

def isRound(p):
    return 'round' in p.keys()

def point(x, y, radius = None, rounding=None):
    'создает словарик для точки'
    res = {'x': x, 'y': y}
    if radius != None:
        res['radius'] = radius
    if rounding != None:
        res['round'] = rounding

    return res

if __name__ == '__main__':
    v = Meta()
    '''
    v.point(20, 20,  rounding=3)
    v.point(30, 20,  rounding=3)
    v.point(30, 10,  rounding=3)
    v.point(45, 20,  radius=-3)
    v.point(60, 10,  radius=5)
    v.point(65, 40,  rounding=3)
    v.point(20, 40)
    
    v2 = Meta()
    v2.point(30, 30,  radius=3)
    v2.point(55, 30,  radius=5)
    v2.jump_point(5,  [19,  70])    

    preview2D([v,  v2],  8)'''
    v.point(17, 18)
    v.point(63, -92)
    v.point(166, -61)
    v.point(210, 93)
    
    
    preview2D(v,  1)

    def f():
        F(300)
        G0(0, 0, 5)
        F(1000)
        x,  y =  v.get_first_position()
        G0(x, y)

        z = -3
        while z > -15:
            G1(Z=z)
            v.to_gcode()
            z -= 3
        G0(Z=5)
        

    preview(f)
#    export(f)
