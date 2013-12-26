# -*- coding: utf-8 -*-

class CNC:
	'Основной класс - внутреннее состояние станка ЧПУ'
	def __init__(self):
		self.__code = [] #список команд
		self.__safe_z = 0

	def __get_pars_G(self, X = None, Y = None, Z = None):
		pars = []
		if X != None: pars.append("X{0}".format(X))
		if Y != None: pars.append("Y{0}".format(Y))
		if Z != None: pars.append("Z{0}".format(Z))
		return pars

	def __append(self, command, args):
		self.__code.append([command, args])		

	def clear(self):
		self.__code = []
	def gcode(self):
		'переводит команды в текстовый вид'
		def com2gcode(com):
			pars = ' '.join(['%s%s' % (k, v) for [k, v] in com[1] if v != None ])
			return com[0] + ' ' + pars
		#TODO: надо оптимизировать: если команда повторяет предыдущую, то ее код писать не обязательно
		return "\n".join([com2gcode(x) for x in self.__code])

	def G0(self, X=None, Y=None, Z=None):
		self.__append("G0", {'X': X, 'Y': Y, 'Z': Z})

	def G1(self, X=None, Y=None, Z=None):
		self.__append("G1", {'X': X, 'Y': Y, 'Z': Z})

	def as_is(self):
		return self.__code
	
	@property
	def safe_z(self):
		'безопасная высота'
		return self.__safe_z

	@safe_z.setter
	def safe_z(self, value):
		self.__safe_z = value


#TODO: вставить матрицу преобразований и метод для работы с ней.
#параметры при вводе должны будут проходить через эту матрицу
