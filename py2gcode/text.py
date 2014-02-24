# -*- coding: utf-8 -*-

from main import *
from group_trajectory import *
from svg import *
from strategy import *
from tool import *
import Fonts

class Char(GroupTrajectory):
    'один символ из svg-строки'
    def __init__(self, dict):
        'на входе словарь из таблицы шрифтов'
        super(Char, self).__init__()
        self.ch = dict['char']
        paths = dict['path'].split('z') #разбиваем на под-траектории

        paths = map(lambda x: x.strip(), paths)
        x, y = None, None #это относительные координаты
        for p in paths: #обрабатываем каждую под-траекторию
            if p != "":
                #TODO: + z потом переделать, когда появятся скелетные шрифты (контуры не замкнутые
                s = SvgTrajectory(p + ' z', x, y) #в шрифтах все контуры замкнутые, поэтому возвращаем по умолчанию                
                x, y = s.get_last_position()
                self.trajectories.append({'svg': s, 'char': dict['char']})

    def min_x(self):
        return min([x['svg'].min_x() for x in self.trajectories])

    def to_left(self):        
        mx = self.min_x()
        for t in self.trajectories:
            for p in t['svg'].points:
                p['x'] -= mx
                
    def offset_y(self, y):
        for t in self.trajectories:
            for p in t['svg'].points:
                p['y'] += y
        
#класс кушает строку и выдает траетории (по одной) для гравировки
class TextTrajectory(GroupTrajectory):
    def __init__(self, font, text):
        super(TextTrajectory,  self).__init__()
        #загружаем модуль со шрифтом
        #mymod = __import__("Fonts." + font)
        #eval("from Fonts.arial import *")
        #fnt = eval("mymod." + font)

        self.text = str
        #разбираем строку на символы, а символы - на траетории
        prev = None
        #offset_y = eval("mymod." + font + ".font_offset_y")
        offset_y = font.font_offset_y
        for ch in text:
            a = font.get_char(ch)
            if a == None and prev != None:
                a = font.get_char(prev + ch)
            if a != None:
                _ch = Char(a)
                _ch.to_left()
                _ch.offset_y(offset_y)                
                self.trajectories += _ch.trajectories
            prev = ch

    def grav(self, x, yy, z, sz, f, size):
        tool = Tool()
        tool.F = f
        cutter = Strategy()
        curr_x = x
        width = 0
        prev_ch = None
        for t in self.trajectories:
            if t['char'] == ' ':
                curr_x += 3*size
                prev_char = ' '
                continue
            if t['char'] != prev_ch and prev_ch != None: #сменилась буква
                curr_x += width + 1*size
                width = 0
            G0(Z = sz)
            cutter.mill(t['svg'], x = curr_x, y = yy, scale=size, options={'z': z, 'safeZ': sz})
            w = t['svg'].width()*size #выбираем максимальную ширину
            if width < w:
                width = w
            prev_ch = t['char']
        G0(Z = sz)

    def get_rect(self, x, y, size):
        'возвращает прямоугольник в абсолютных координатах'
        x_left = x
        y_bottom = y
        x_right = x
        y_top = y
        curr_x = x
        width = 0
        prev_ch = None        
        for t in self.trajectories:       
            if t['char'] == ' ' :
                curr_x += 3*size
                prev_char = ' '
                continue
            if t['char'] != prev_ch and prev_ch != None: #сменилась буква
                curr_x += width + 1*size
                width = 0
            for p in t['svg'].points:
                xx = p['x']*size + curr_x
                yy = p['y']*size + y
                if x_left > xx: x_left = xx
                if x_right < xx: x_right = xx
                if y_bottom > yy: y_bottom = yy
                if y_top < yy: y_top = yy
                
                    
            #cutter.grav(t['svg'], tool, curr_x, y, z, size)
            w = t['svg'].width()*size #выбираем максимальную ширину
            if width < w:
                width = w
            prev_ch = t['char']
            
        return x_left, y_bottom, x_right, y_top

if __name__ == '__main__':
    def f():
        G0(0, 0, 5)
        from Fonts import arial

        font = arial
        t = TextTrajectory(arial, "Иван Вячеславович")
        sz = 5
        t.grav(0, 0, -1, sz, 500, 3)
        G0(0, 0)
        x1, y1, x2, y2 = t.get_rect(0, 0, 3)
        G0(x1, y1)
        G1(Z=-1)
        G1(x2, y1)
        G1(x2, y2)
        G1(x1, y2)
        G1(x1, y1)
    
        #preview2D([x['svg'] for x in t.trajectories], 10)
    #f()
    preview(f)
    #export(f)


