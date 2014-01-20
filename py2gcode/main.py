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

def com2text(g):
	'конвертирует запись в текстовый вид'
	print g
	res = g[0]
	pars = g[1]
	if 'X' in pars and pars['X'] != None:
		res += (" X%s" % pars['X'])

	if 'Y' in pars and pars['Y'] != None:
		res += (" Y%s" % pars['Y'])

	if 'Y' in pars and pars['Z'] != None:
		res += (" Z%s" % pars['Z'])

	if 'value' in pars and pars['value'] != None:
		res += ("%s" % pars['value'])

	return res

def export(function):
	'Экспортирует результат выполнения функции в файл'
	function()
	#myfile = open(filename,'w')
	for l in __cnc__.as_is():
		print com2text(l)
		#myfile.write(com2text(l) + "\n")
	#myfile.close()
	#print __cnc__.as_is()
	print "m2"


def preview(function):
	'выводит на экран траекторию работы программы'
	v = Viewer(function)
	v.show()


def path(com, str):
	'''путь на микроязыке'''
	pass


#всякие команды
def G0(X = None, Y = None, Z = None): 
	'быстрое перемещение'
	__cnc__.G0(X, Y, Z)

def G1(X = None, Y = None, Z = None): 
	'рабочее перемещение'
	__cnc__.G1(X, Y, Z)


def F(value):
	__cnc__.F(value)

