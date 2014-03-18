# -*- coding: utf-8 -*-

from main import *
from trajectory import *
from tool import *
from geometry import *

default_safeZ = 5

#базовый класс, генерирующий Г-код для одной траектории. Так же уже умеет вырезать по контуру
class Strategy(object):
    def __init__(self):
        pass    
    
    '''def cut_on_line(self, trajectory, z_start, z_stop, z_step, z_safe, tool, options=None):
        #вырезает по средней линии
        #    z_start - глубина первого прохода
        #    z_stop - глубина последнего прохода
        #    z_step -  с каким шагом заглубляться
        #    tool - каким инструментом
        #    options - всякие опции
        #    если есть перемычки, то их толщина будет 1.5 мм
        
        trajectory.create_trajectory
        G0(Z = z_safe)
            
        z = z_start
        while z >= z_stop:
            self.__one_z_level(trajectory, tool, z, z_stop + 1.5)
            z -= z_step'''
            
    def get_xy(self, x, y, scale, angle):
        'возвращает функцию, которая пересчитывает координаты в зависимости от всех параметров'
        def xy(xx, yy): #считает координута с учетом всех параметров (масштаб, разворот
            rx, ry = xx, yy
            if angle != None:
                nx = rx*cos(angle) - ry*sin(angle)
                ny = rx*sin(angle) + ry*cos(angle)
                rx, ry = nx, ny
            return rx*scale + x, ry*scale + y
        return xy

    def mill(self, tr, tool=Tool(), x=0, y=0, scale=1, angle=None, options={}):
        'режем без всяких перемычек и прочего'
        #если задан угол, то поворачиваем
        safeZ = main.get_option(options, 'safeZ', default_safeZ)
        
        xy = self.get_xy(x, y, scale, angle)
        fx, fy = tr.get_first_position()
        fx, fy = xy(fx, fy)
        G0(Z=safeZ)
        G0(fx, fy)
        zz = get_option(options, 'z', None)
        if zz != None:
            #погружаемся
            F(tool.FZ)
            G1(Z=zz)
        F(tool.F)
        points = tr.get_next_point() 
        points.next()  #первую точку пропускаем, мы взяли ее с помощью get_first_position
        for p in points:
            xx, yy = xy(p['x'], p['y'])
            G1(xx,  yy)

    def __one_z_level(self, trajectory, tool, z, z_up=None):
        x, y = trajectory.get_first_position()
        G0(x, y)
        #погружаемся
        F(tool.FZ)
        G1(Z=z)
        F(tool.F)

        if len(trajectory.jump_points) == 0:  #плоская траектория, без всяких перемычек
            #pp = trajectory.get_next_point() #первую точку пропускаем, мы взяли ее с помощью get_first_position
            points = trajectory.get_next_point() 
            points.next()  #первую точку пропускаем, мы взяли ее с помощью get_first_position
            for p in points:
                G1(p['x'],  p['y'])
        else: #код с учетом перемычек
            curr_z = z
            points = trajectory.get_next_point() 
            points.next() #первую точку пропускаем, мы взяли ее с помощью get_first_position
            for p in points: #trajectory.get_next_point():                
                if p['type'] == 'f':
                    if curr_z != z: #чтобы бесконечно не гонять G1 Z
                        F(tool.FZ)
                        G1(Z = z)
                        F(tool.F)
                        curr_z = z
                    G1(X=p['x'],  Y=p['y'])
                else:
                    if z < z_up:
                        if curr_z != z_up:
                            G0(Z = z_up)
                            curr_z = z_up
                    G1(X=p['x'],  Y=p['y'])

if __name__ == '__main__':
    from meta import Meta
    v = Meta()

    v.point(0, 0)
    v.point(200, 0)

    v.point(200, 70)
    v.point(170, 70)
    v.point(170, 120)
    v.point(200, 120)

    v.point(200, 200)
    v.point(0, 200)
    v.point(0, 120)
    v.point(-50, 95)
    v.point(0, 70)

    #v.jump_point(20, [10, 60])

    preview2D(v,  2)

    def f():
        G0(0, 0, default_safeZ)
        cut = Strategy()
        cut.mill(v, x=-10, y=-10, options={'z': -10})

    preview(f)
