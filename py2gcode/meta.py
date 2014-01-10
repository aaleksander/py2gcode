# -*- coding: utf-8 -*-
from Tkinter import *
from geometry import *


#построение мета-траекторий, т.е. замкнутых траекторий на основе каких-то опорных точек и с помощью "эластичной ленты" вокруг всех точек
'''
опорная точка - это словарь со следующими полями
x, y - координата
radius - радиус точки, по умолчанию - ноль
relative - точка внутри или снаружи
	in - точка всегда внутри метатраектории
	out - точка снаружи метатраектории
	None - по умолчанию - внутри
'''
#TODO: добавить матричные операции (повернуть на угол, отразить, растянуть)

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

		#посчитаем масштаб, чтобы все помещалось на экране

		#рисуем
		self.canvas.delete('all')

		for p in self.points:
			x = p['x']
			y = p['y']
			self.__drawPoint(x, y)
			if 'radius' in p.keys():
				r = p['radius']				
  				self.canvas.create_oval(x - r, y - r, x + r, y + r, outline='red')

		self.canvas.create_line(self.__path, fill='red', arrow = LAST, arrowshape = (15, 20, 5))

	def __drawPoint(self, x, y):
		size = 5
		self.canvas.create_line(x, y - size, x, y + size, fill='yellow')
		self.canvas.create_line(x - size, y, x + size, y, fill='yellow')

	def __create_path(self):
		'создает траекторию по self.points'
		self.__path = []
		
		prev = {}
		for p in self.points:
			pp = self.__get_segment(prev, p)			
			if len(pp) == 0:
				prev = p.copy()
				
			if len(pp) == 2:
				self.__path.append(pp[0].x)
				self.__path.append(pp[0].y)
				prev['x'] = pp[1].x
				prev['y'] = pp[1].y

		self.__path.append(self.points[0]['x'])
		self.__path.append(self.points[0]['y'])
		print "ok: ", self.__path


	def __get_segment(self, p1, p2):
		if p1 == None or len(p1) == 0:
			return ()

		if isCircle(p1)
		return (Point(p1['x'], p1['y']), Point(p2['x'], p2['y']))

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
	pp.append( point(100, 100) )
	pp.append( point(200, 100) )
	pp.append( point(250, 200, 20) )
	pp.append( point(200, 300) )
	pp.append( point(100, 300) )
	pp.append( point(120, 200) )

	v = MetaViewer(pp)
	v.show()

