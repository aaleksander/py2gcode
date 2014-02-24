# -*- coding: utf-8 -*-

#визуализация плоской траектории (Trajectory, Meta) в окошке

from Tkinter import *
from cnc import *
from math import cos, sin
import main
from cnc import *




class Viewer2D:
    'Просмотрщик'
    def __init__(self,  trajectoryes,  scale):
        'задаем на вход массив траекторий'
        
        #возможность принимать на вход не массив, а одинокую траекторию
        if isinstance(trajectoryes, list):
            self._trajectoryes = trajectoryes
        else:
            self._trajectoryes = [trajectoryes]
        #последние мышиные координаты
        self.last_x = -1
        self.last_y = -1

        #сдвиг сцены
        self.scroll_x = 0
        self.scroll_y = 0

        self._zoom = scale

        #размеры холста
        self.size_x = 1024
        self.size_y = 768

        #инициализация интерфейса
        self.root = Tk()

        self.root.title("Simple Graph")        
        
        self.c = Canvas(self.root, bg="white", width=self.size_x, height=self.size_y)
        self.c.configure(background='black')
        #self.c.configure(cursor="crosshair")
        self.c.pack()

        #назначаем события мыши
        self.c.bind("<Button-1>", self.down1)
        self.c.bind("<ButtonRelease-1>", self.up1)
        self.c.bind("<Button-3>", self.down1)
        self.c.bind("<ButtonRelease-3>", self.up1)
        self.c.bind("<Button-2>", self.down1)
        self.c.bind("<ButtonRelease-2>", self.up1)

        self.c.bind("<B1-Motion>", self.scroll)
        
        self.root.bind("<MouseWheel>", self.zoom)        
        
        self.scroll_y = self.size_y - 10
        self.scroll_x = 10

    def zoom(self, event):
        'зуминг сцены'
        self._zoom -= event.delta/1200.0
        if self._zoom < 0.1:
            self._zoom = 0.1
        self.draw()

    def show(self):
        self.draw()
        self.root.mainloop()

    def add_point(self, x, y, z, t):
        'добавление точки'		
        self.points.append(Point_v(x, y, -z, t))

    def down1(self, event):
        'вдавили левую кнопку'
        self.last_x = event.x
        self.last_y = event.y

    def up1(self, event):
        'отпустили левую кнопку'
        self.last_x = -1
        self.last_y = -1

    def scroll(self, event):
        'скроллируем сцену'
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.scroll_x += dx
        self.scroll_y += dy
        self.last_x = event.x;
        self.last_y = event.y;
    #перерисовыаем
        self.draw()

    def draw(self):
        'рисуем сцену с учетом всех вращений, преобразований и сдвигов'
        self.c.delete('all')       

        #перекрестие по нулям
        self.c.create_line(0,  self.scroll_y,  1000,  self.scroll_y,  fill="white",  width=1)
        self.c.create_line(self.scroll_x,  0,  self.scroll_x, 1000,   fill="white",  width=1)

        for t in self._trajectoryes:
            t.draw(self.c,  self.scroll_x,  self.scroll_y,  self._zoom)
