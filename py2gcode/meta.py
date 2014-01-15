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


#типы сегменто
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
		'''возвращает список координт, готовый для рисования на канве
		т.е. просто список: x, y, x, y, x, y, x, y, x, y ...		'''

		def get_line_for_arc(p1, center, p2):
			'считает линии для дуги от точки до точки и с центром'
			#считаем начальный угол
			zero = Point(center.x + 100, center.y)
			a1 = get_angle(center, self.p1, center, zero)
			a2 = get_angle(center, self.p2, center, zero)

			if self.radius < 0:
				a1, a2 = a2, a1

			if a1 < a2:
				a1 += 2*pi

			r = dist(center, self.p1)
			res = []
			while a1 > a2:
				res.append(center.x + r*cos(a1))
				res.append(center.y - r*sin(a1))
				a1 = a1 - 0.1

			#последний шажок, если в цикле "перебежали"
			if a1 < a2:
				res.append(center.x + r*cos(a2))
				res.append(center.y - r*sin(a2))
			return res


		if self.type == SEG_ARC: #скругляем дугу относительно центра
			res = get_line_for_arc(self.p1, self.center, self.p2)
		else:
			#расчитываем, откуда будет начинаться дуга

			zero = Point(self.center.x + 1000, self.center.y)
			
			a1 = get_angle(self.center, self.p1, self.center, zero)
			a2 = get_angle(self.center, self.p2, self.center, zero)		
			if a2 < a1:
				a2 += pi*2	
			#a1 = get_angle(self.p1, self.center, self.center, zero)
			#a2 = get_angle(self.p1, self.center, self.center, self.p2) + a1
			middle = (a1 + a2)/2.0			
  			
			rr = self.radius/sin(middle)#acos(middle - a1)*self.radius

			if middle <= pi:
				center = [self.center.x + rr*cos(middle), self.center.y - rr*sin(middle)]
			else:
				center = [self.center.x - rr*cos(middle), self.center.y + rr*sin(middle)]
			print self.center, a1*180.0/pi, a2*180.0/pi, middle*180.0/pi, center
			print

			#находим начальную и конучную точки дуги

  			if( canvas != None ):
  				canvas.create_oval(
  					center[0] - self.radius, center[1] - self.radius,
  					center[0] + self.radius, center[1] + self.radius, outline='blue')

#			p1 = contact_points(self.center, Circle(center[0], center[1], self.radius))[0]
#			p2 = contact_points(self.center, Circle(center[0], center[1], self.radius))[1]

 # 			res = [p1.x, p1.y, p2.x, p2.y]

			#res = get_line_for_arc(self.p1, 
			#	Point(self.center.x + rr*cos(middle), self.center.y - rr*sin(middle)), 
			#	self.p2)

			#res += center

			#res = get_line_for_arc(self.p1, self.center, self.p2)
			res = [	self.center.x, self.center.y, 
					self.center.x + self.radius*cos(middle),
					self.center.y - self.radius*sin(middle)]

		return res

	def to_gcode(self):
		ll = self.get_lines()
		pair = lambda arr: [arr[i:i + 2] for i in range(0, len(arr), 2)]	#разбивает на пары

		ll = pair(ll)
		if self.radius < 0:
			ll.reverse()

		for l in ll:
			G1(l[0], l[1])

	def round(self, p1, p2):
		'скругляем сегмент'
#		self.center = Point(self.center.x - 5, self.center.y - 5)
		self.p1 = Point(
			(self.center.x + p1.x)/2,
			(self.center.y + p1.y)/2)
		self.p2 = Point(
			(self.center.x + p2.x)/2,
			(self.center.y + p2.y)/2)

		#print self.p1
		#print self.p2


class Meta:
	'Метатраектория'
	def __init__(self):
		#точки должны быть в том порядке, в каком будет обход
		self.points = []
		#self.__create_path()


	def point(self, x, y, radius=None, rounding=None):
		self.points.append( point(x, y, radius, rounding))
		if len(self.points) > 1:
			self.__create_path()

	def show(self, scale = 1):
		self.draw(scale)
		self.root.mainloop()

	def draw(self, scale):
		'рисуем сцену с учетом всех вращений, преобразований и сдвигов'
		self.root = Tk()

		self.root.title("MetaViewer")
		self.canvas = Canvas(self.root, bg="white", width=640, height=480)
		self.canvas.configure(background='black', width=800, height=600)
		#self.c.configure(cursor="crosshair")
		self.canvas.pack()

		#рисуем
		self.canvas.delete('all')

		#рисуем все точки в виде желтых окружностей с перекрестием
		
		for p in self.points:
			x = p['x']*scale
			y = p['y']*scale
			self.__drawPoint(x, y)
			if 'radius' in p.keys():
				r = p['radius']				
  				self.canvas.create_oval(x - r*scale, y - r*scale, x + r*scale, y + r*scale, outline='yellow')

  		#рисуем путь
  		for s in self.__path:
  			if s.type == SEG_LINE:
  				self.canvas.create_line(s.p1.x*scale, s.p1.y*scale, s.p2.x*scale, s.p2.y*scale, fill='red')
  			if s.type == SEG_ARC:
  				self.canvas.create_line(map(lambda x: x*scale, s.get_lines()), fill='red')#, arrow = LAST, arrowshape = (15, 20, 5))
  			if s.type == SEG_ROUND: 				

  				self.canvas.create_line(map(lambda x: x*scale, s.get_lines(self.canvas)), fill='red')#, arrow = LAST, arrowshape = (15, 20, 5))

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
		stack = [] #тут будем запоминать предыдущие значения

		prev = self.points[0]
		prevO = None#Point(None, None)
		first = True
		for p in self.points[1:]:
			pp = self.__get_segment(prev, p) #расчитываем сегмент
			if prevO != None: #сохраняем в стэке предыдущее значение
				stack.insert(0, prevO)
			if len(pp) == 2:
				if isRound(prev) and first == True: #первая точка - скругление
					#pp = Point(p.x, p.y)					
					self.__path.append(Segment(SEG_ROUND, prev, prev, Point(prev['x'], prev['y']), prev['round']))

				if isCircle(prev) and first == False:#если предыдущая точка была окружность, то вставляем дугу
					self.__path.append(Segment(SEG_ARC, prevO, pp[0], Point(prev['x'], prev['y']), prev['radius']))

				if isRound(prev) and first == False:#скругляем угол
					self.__path.append(Segment(SEG_ROUND, p, p, prevO, prev['round']))

				self.__path.append(Segment(SEG_LINE, pp[0], pp[1]))
				prevO = pp[1].copy()

			prev = p.copy() #запоминаем предыдущую точку
			first = False

		#завершаем контур
		pp = self.__get_segment(prev, self.points[0])

		if isCircle(prev):#если предыдущая точка была окружность, то вставляем дугу
			self.__path.append(Segment(SEG_ARC, prevO, pp[0], Point(prev['x'], prev['y']), prev['radius']))

		if isRound(prev):#скругляем угол
			self.__path.append(Segment(SEG_ROUND, p, p, prevO, prev['round']))


		self.__path.append(Segment(SEG_LINE, pp[0], pp[1]))

		if isCircle(self.points[0]):			
			self.__path.append(Segment(SEG_ARC, pp[1], self.__path[0].p1, Point(self.points[0]['x'], self.points[0]['y']), self.points[0]['radius']))

		#проходим по траектории и скругляем углы (round)

		new_path = []
		for i in xrange(0, len(self.__path)):
			s = self.__path[i]
			if s.type == SEG_ROUND:
				s_prev = get_from_ring(self.__path, i, -1)
				s_past = get_from_ring(self.__path, i, 1)
				s.round(s_prev.p1, s_past.p2) #скругляем

				#заменяем нашу вершину на дуугу (всталяем в середину пути)


		#if isRound(self.points[0]):
		#	self.__path.append(Segment(SEG_LINE, pp[1], self.__path[0].p1))

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
			#raise Exception("Пока что две окружности подряд не поддерживаются")

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
#	v.point(50, 10, 10)
#	v.point(70, 80, -10)
#	v.point(100, 100, 10)
#	v.point(70, 120, -10)
#	v.point(50, 190, 10)
#	v.point(30, 100, 30)

	v.point(200, 200, rounding=30)
	v.point(300, 200, rounding=-30)
	
	v.point(350, 100, rounding=10) #^

	v.point(450, 200, rounding=-30)
	v.point(700, 200, rounding=30) 
	v.point(600, 400, rounding=30) 

	v.point(450, 400, rounding=-20)
	v.point(350, 500, rounding=20)
	v.point(300, 400, rounding=-20)

	v.point(200, 400, rounding=30) 

	v.show()