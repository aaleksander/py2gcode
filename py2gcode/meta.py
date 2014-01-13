# -*- coding: utf-8 -*-
from Tkinter import *
from geometry import *
from math import cos, sin
from main import *


#построение мета-траекторий, т.е. замкнутых траекторий на основе каких-то опорных точек и с помощью "эластичной ленты" вокруг всех точек
'''
опорная точка - это словарь со следующими полями
x, y - координата
radius - радиус точки, по умолчанию - ноль
	- если радиус отрицательный, то траектория его "обойдет" с другой стороны
'''
#TODO: добавить матричные операции (повернуть на угол, отразить, растянуть)

#типы сегменто
SEG_LINE	= 1 #прямая лини
SEG_ARC 	= 2 #дуга
class Segment:
	'''
		Один сегмент пути
	'''

	def __init__(self, type, p1, p2, center = None, radius = None):
		'создает сегмент типа дуга, p1, p2 - начало конец, p3 - центр'
		self.type = type
		self.p1 = p1.copy()
		self.p2 = p2.copy()
		if center != None:
			self.center = center.copy()
		if radius != None:
			self.radius = radius

	def draw(self, canvas, color):
		'рисуем сегмент на канве'
		pass

	def __str__(self):
		return "%(t)s, %(p1)s, %(p2)s" % {'t': self.type, 'p1': self.p1, 'p2': self.p2}


	def get_lines(self):
		'''возвращает список координта, готовый для рисования на канве
		т.е. просто список: x, y, x, y, x, y, x, y, x, y ...		'''
		
		#считаем начальный угол
		zero = Point(self.center.x + 100, self.center.y)
		a1 = get_angle(self.center, self.p1, self.center, zero)
		a2 = get_angle(self.center, self.p2, self.center, zero)

		if self.radius < 0:
			a1, a2 = a2, a1

		if a1 < a2:
			a1 += 2*pi

		r = dist(self.center, self.p1)
		res = []
		while a1 > a2:
			res.append(self.center.x + r*cos(a1))
			res.append(self.center.y - r*sin(a1))
			a1 = a1 - 0.1

		if a1 < a2:
			res.append(self.center.x + r*cos(a2))
			res.append(self.center.y - r*sin(a2))

		return res

	def to_gcode(self):
		ll = self.get_lines()
		pair = lambda arr: [arr[i:i + 2] for i in range(0, len(arr), 2)]	 #разбивает на пары

		ll = pair(ll)
		if self.radius < 0:
			ll.reverse()

		for l in ll:
			G1(l[0], l[1])


class Meta:
	'Просмотрщик метатраектории'
	def __init__(self, points):
		#точки должны быть в том порядке, в каком будет обход
		self.points = points


		self.__create_path()

	def show(self):
		self.draw()
		self.root.mainloop()

	def draw(self):
		'рисуем сцену с учетом всех вращений, преобразований и сдвигов'
		self.root = Tk()

		self.root.title("MetaViewer")
		self.canvas = Canvas(self.root, bg="white", width=640, height=480)
		self.canvas.configure(background='black')
		#self.c.configure(cursor="crosshair")
		self.canvas.pack()

		#посчитаем масштаб, чтобы растянуть/уместить все на экран

		#рисуем
		self.canvas.delete('all')

		#рисуем все точки в виде желтых окружностей с перекрестием
		for p in self.points:
			x = p['x']
			y = p['y']
			self.__drawPoint(x, y)
			if 'radius' in p.keys():
				r = p['radius']				
  				self.canvas.create_oval(x - r, y - r, x + r, y + r, outline='yellow')

  		#рисуем путь
  		for s in self.__path:
  			if s.type == SEG_LINE:
  				self.canvas.create_line(s.p1.x, s.p1.y, s.p2.x, s.p2.y, fill='red')
  			if s.type == SEG_ARC:
  				self.canvas.create_line(s.get_lines(), fill='red')#, arrow = LAST, arrowshape = (15, 20, 5))


	def to_gcode(self, z):
		'отправляем все в Г-код на определенную глубина'
		first = False
  		for s in self.__path:
  			if s.type == SEG_LINE:
  				if first == False:
  					G0(s.p1.x, s.p1.y)
  					G1(Z = z)
  					first = True
  				G1(s.p2.x, s.p2.y)
  			if s.type == SEG_ARC:
  				s.to_gcode()
  				G1(s.p2.x, s.p2.y)


	def __drawPoint(self, x, y):
		size = 5
		self.canvas.create_line(x, y - size, x, y + size, fill='yellow')
		self.canvas.create_line(x - size, y, x + size, y, fill='yellow')


	def __create_path(self):
		'создает траекторию по self.points'
		self.__path = []

		prev = self.points[0]
		prevO = Point(None, None)
		first = True
		for p in self.points[1:]:
			pp = self.__get_segment(prev, p)

			if len(pp) == 2:			
				if isCircle(prev) and first == False:#если предыдущая точка была окружность, то вставляем дугу				
					self.__path.append(Segment(SEG_ARC, prevO, pp[0], Point(prev['x'], prev['y']), prev['radius']))
				self.__path.append(Segment(SEG_LINE, pp[0], pp[1]))
				prevO = pp[1].copy()

			prev = p.copy()
			first = False

		pp = self.__get_segment(prev, self.points[0])

		if isCircle(prev):#если предыдущая точка была окружность, то вставляем дугу
			self.__path.append(Segment(SEG_ARC, prevO, pp[0], Point(prev['x'], prev['y']), prev['radius']))
		self.__path.append(Segment(SEG_LINE, pp[0], pp[1]))

		if isCircle(self.points[0]):			
			self.__path.append(Segment(SEG_ARC, pp[1], self.__path[0].p1, Point(self.points[0]['x'], self.points[0]['y']), self.points[0]['radius']))


	def __get_segment(self, p1, p2):
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
			#raise Exception("Пока что две окружности подряд не поддерживаются")

		return (Point(p1['x'], p1['y']), Point(p2['x'], p2['y']))


def dict2object(o):
	'преобразует словарик в точку или окружность'
	if isCircle(o):
		return Circle(o['x'], o['y'], o['radius'])
	return Point(o['x'], o['y'])


def isCircle(p):
	return 'radius' in p.keys()

def point(x, y, radius = None):
	'создает словарик для точки'
	res = {'x': x, 'y': y}
	if radius != None:
		res['radius'] = radius
	return res


if __name__ == '__main__':
	pp = []
	pp.append( point(100, 100, 30.0) )
	pp.append( point(400, 100, 50.0) )
	pp.append( point(400, 300, 30) )
	pp.append( point(300, 200, -50) )
	pp.append( point(100, 300, 30) )

#	pp.append( point(100, 100, 30) )
#	pp.append( point(300, 80, 20) )
#	pp.append( point(130, 130, -10) )
#	pp.append( point(80, 300, 20) )

	v = Meta(pp)
	v.show()

