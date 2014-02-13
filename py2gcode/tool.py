# -*- coding: utf-8 -*-

from main import *

#класс инструмент. Хранит настройки инструмента

class Tool:
    def __init__(self, diameter=3, FZ = 300, F=3000):
        self.diameter = diameter    #диаметр инструмента
        self.FZ = FZ                    #вертикальная подача
        self.F = F                        #горизонтальная подача  
