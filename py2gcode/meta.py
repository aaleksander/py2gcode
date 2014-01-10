# -*- coding: utf-8 -*-
from Tkinter import *


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
		self.points = points
		self.root = Tk()

		self.root.title("MetaViewer")

		self.canvas = Canvas(self.root, bg="white", width=640, height=480)
		self.canvas.configure(background='black')
		#self.c.configure(cursor="crosshair")
		self.canvas.pack()

	def show(self):
		self.draw()
		self.root.mainloop()

	def draw(self):
		'рисуем сцену с учетом всех вращений, преобразований и сдвигов'
		self.canvas.delete('all')




def show(path):
	#показывает траекторию в 2D
	pass


if __name__ == '__main__':
	pp = []
	pp.append({'x': 100, 'y': 100})
	pp.append({'x': 120, 'y': 70})
	pp.append({'x': 70,  'y': 60})

	v = MetaViewer(pp)
	v.show()

