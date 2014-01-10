# -*- coding: utf-8 -*-
from Tkinter import *
from geometry import *


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

class MetaViewer:
	'Просмотрщик метатраектории'
	def __init__(self, points):
		#точки должны быть в том порядке, в каком будет обход
		self.points = points
		self.root = Tk()

		self.root.title("MetaViewer")

		self.canvas = Canvas(self.root, bg="white", width=640, height=480)
		self.canvas.configure(background='black')
		#self.c.configure(cursor="crosshair")
		self.canvas.pack()

		self.__create_path()

	def show(self):
		self.draw()
		self.root.mainloop()

	def draw(self):
		'рисуем сцену с учетом всех вращений, преобразований и сдвигов'
		#посчитаем масштаб, чтобы растянуть/уместить все на экран

		#рисуем
		self.canvas.delete('all')

		for p in self.points:
			x = p['x']
			y = p['y']
			self.__drawPoint(x, y)
			if 'radius' in p.keys():
				r = p['radius']				
  				self.canvas.create_oval(x - r, y - r, x + r, y + r, outline='yellow')

  		for s in self.__path:
  			print s

  		for s in self.__path:
  			if s.type == SEG_LINE:
  				self.canvas.create_line(s.p1.x, s.p1.y, s.p2.x, s.p2.y, fill='red')
  			if s.type == SEG_ARC:
  				#вычислить углы и проинтерполировать
  				#print s
  				self.canvas.create_line(s.p1.x, s.p1.y, s.p2.x, s.p2.y, fill='blue', arrow = LAST, arrowshape = (15, 20, 5))
  				#self.canvas.create_arc(s.p1.x, s.p1.y, s.p2.x, s.p2.y, outline='blue')

		#self.canvas.create_line(self.__path, fill='red', arrow = LAST, arrowshape = (15, 20, 5))

	def __drawPoint(self, x, y):
		size = 5
		self.canvas.create_line(x, y - size, x, y + size, fill='yellow')
		self.canvas.create_line(x - size, y, x + size, y, fill='yellow')


	#TODO: сделать, чтобы можно было сделать две окружности подряд
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
			raise Exception("Пока что две окружности подряд не поддерживаются")

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
	pp.append( point(100, 100, 20) )
	pp.append( point(200, 100) )
	pp.append( point(200, 300, 20) )
	pp.append( point(100, 300) )
	#pp.append( point(200, 300) )
	#pp.append( point(100, 300, 10) )
	#pp.append( point(120, 200) )

	v = MetaViewer(pp)
	v.show()

