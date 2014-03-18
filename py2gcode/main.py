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

def get_font(str):
    import sys
    return sys.modules["py2gcode.Fonts." + str]
    #return __import__("py2gcode.Fonts." + str)

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

def preview2D(trajectoryes,  scale, options = None):
	'выводит на экран траекторию работы программы'
	Viewer2D(trajectoryes,  scale, options).show()

def path(com, str):
	'''путь на микроязыке'''
	pass

#всякие команды
def G0(X = None, Y = None, Z = None): 
    'быстрое перемещение'
    __cnc__.G0(X, Y, Z)

    #print "G0 ", X, Y, Z
    
def G1(X = None, Y = None, Z = None, F=None): 
    'рабочее перемещение'
    if F != None:
        __cnc__.F(F)
    __cnc__.G1(X, Y, Z)
    
    #print "G1 ", X, Y, Z

def F(value):
    __cnc__.F(value)

def get_option(options, key, default):
    'берет из словаря какое-то значение по ключу, либо возвращает значение по умолчанию'
    if options == None:
        return default
    if not key in options:
        return default
    return options[key]

def mill(traj, z_start=0, z_stop=None, z_step = 1, FF=3000, FZ=200, options=None):
    'вырезаем траекторию'
    from strategy import Strategy
    from tool import Tool
    cut = Strategy()
    t = Tool()
    t.F = FF
    t.FZ = FZ
    #берем опции
    xx = get_option(options, 'x', 0)
    yy = get_option(options, 'y', 0)
    sc = get_option(options, 'scale', 1)
    ang = get_option(options, 'angle', 0)

    if z_stop == None: #просто один слой там, где скажут
        cut.mill(traj, tool=t, x=xx, y=yy, scale=sc, angle=ang, options=options)
        return

    opt = options.copy()
    z = z_start
    while z >= z_stop:
        opt['z'] = z
        cut.mill(traj, tool=t, x=xx, y=yy, scale=sc, angle=ang, options=opt)        
        z -= z_step

    if z + z_step > z_stop: #дорезаем остатки
        opt['z'] = z_stop
        cut.mill(traj, tool=t, x=xx, y=yy, scale=sc, angle=ang, options=opt)        

def mill_offset(traj, off = 3, z_start=0, z_stop=None, z_step = 1, FF=3000, FZ=200, options=None):
    from offset import Offset
    new_tr = Offset(traj, off)
    mill(new_tr, z_start, z_stop, z_step, FF, FZ, options)
    
    
    
    
    
    
