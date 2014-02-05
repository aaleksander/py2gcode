# -*- coding: utf-8 -*-
import dis
from cnc import *
from viewer3D import *
from viewer2D import *


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
    def format(pp,  par):
        if par in pp and pp[par] != None:
            return (" %(n)s%(v)s" % {'n': par, 'v': pp[par]})
        else:
            return ""

    res = g[0]
    pars = g[1]
    res += format(pars,  'X')
    res += format(pars,  'Y')
    res += format(pars,  'Z')

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
	Viewer3D(function).show()

def preview2D(trajectoryes,  scale):
	'выводит на экран траекторию работы программы'
	Viewer2D(trajectoryes,  scale).show()

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

