# -*- coding: utf-8 -*-
import dis
from cnc import *
from viewer import *


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

def programm(function):
	'возвращает программу в виде массива'
	function()
	return __cnc__.as_is()

def export(function, filename):
	'Экспортирует результат выполнения функции в файл'
	function()
	print __cnc__.as_is()


def preview(function):
	'выводит на экран траекторию работы программы'
	v = Viewer(function)
	v.show()

#всякие команды
def G0(X = None, Y = None, Z = None): 
	'быстрое перемещение'
	__cnc__.G0(X, Y, Z)

def G1(X = None, Y = None, Z = None): 
	'рабочее перемещение'
	__cnc__.G1(X, Y, Z)




