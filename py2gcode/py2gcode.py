# -*- coding: utf-8 -*-
import dis
from cnc import *
from Tkinter import *


__cnc__ = CNC()

def clearCNC():
	'очистить УП'
	__cnc__.clear()

#декоратор для конечной функции УП
def cnc(function):
	'декоратор'
	def wrap():	
		function()
		return __cnc__.gcode()	
	return wrap


def export(function, filename):
	'Экспортирует результат выполнения функции в файл'
	print function()


def preview(function):
	'выводит на экран траекторию работы программы'
	master = Tk()

	w = Canvas(master, width=200, height=100)
	w.pack()

	w.create_line(0, 0, 200, 100)
	w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

	w.create_rectangle(50, 25, 150, 75, fill="blue")

	mainloop()

#всякие команды
def G0(X = None, Y = None, Z = None): 
	'быстрое перемещение'
	__cnc__.G0(X, Y, Z)

def G1(X = None, Y = None, Z = None): 
	'рабочее перемещение'
	__cnc__.G1(X, Y, Z)




