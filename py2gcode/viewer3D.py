# -*- coding: utf-8 -*-

#визуализация УП в окошке

from Tkinter import *
from cnc import *
from math import cos, sin
from cnc import *

'''
управление как в LinuxCNC:
левая кнопка - скролл
правая - зум
средняя - вращать
'''

class Point_v:
	'точка'
	def __init__(self, x, y, z, t):
		self.x = x
		self.y = y
		self.z = z
		self.type = t

	@property
	def X(self):
		return self.x
	
	@property
	def Y(self):
		return self.y

	@property
	def Z(self):
		return self.z

	@property
	def Type(self):
		'Тип перемещения к следующей точке'
		return self.type

	def rot_x(self, a):
		'вращаем точку вокруг х на градус а. Возвращает новую точку'
		y = self.Y*cos(a) - self.Z*sin(a)
		z = self.Y*sin(a) + self.Z*cos(a)
		return Point_v(self.X, y, z, self.Type)

	def rot_y(self, a):
		x = self.X*cos(a) + self.Z*sin(a)
		z = -self.X*sin(a) + self.Z*cos(a)
		return Point_v(x, self.Y, z, self.Type)

	def rot_z(self, a):
		x = self.X*cos(a) - self.Y*sin(a)
		y = self.X*sin(a) + self.Y*cos(a)
		return Point_v(x, y, self.X, self.Type)

class Viewer3D:
    'Просмотрщик'
    def __init__(self, function):
        self.function = function #функция, результат которой надо визуализировать
        #последние мышиные координаты
        self.last_x = -1
        self.last_y = -1

        #сдвиг сцены
        self.scroll_x = 0
        self.scroll_y = 0

        self._zoom = 70

        #размеры холста
        self.size_x = 1300
        self.size_y = 1000

        #вращение
        self.rot_x = -120
        self.rot_y = 90

        #инициализация интерфейса
        self.root = Tk()

        self.root.title("Simple Graph")

        #self.root.resizable(0,0)

        self.points = []

        spline = 0

        tag1 = "theline"

        #добавляем в сцену кубик
        s = 90

        #получаем список команд        
        from main import programm
        comm = programm(function)
        
        #print comm
        #обработка разных команд
        lx = None
        ly = None
        lz = None
        def getVal(dic, key, default): 
            'получаем из словаря значение по ключу key'
            if( key in dic.keys() ):
                if( dic[key] != None ):
                    return dic[key]
            return default
        noStart = True
        for c in comm:
            if c[0] not in ['G0',  'G1',  'G2',  'G3']:
                continue
            if( c[0] == 'G0' ):
                g = 'white'
            else:
                g = 'red'
            lx = getVal(c[1], 'X', lx)
            ly = getVal(c[1], 'Y', ly)
            lz =  getVal(c[1], 'Z', lz)
            if( lx != None and ly != None and lz != None and noStart == True):
                noStart = False
                self.add_point(lx, ly, lz, g)	
            self.add_point(lx, ly, lz, g)

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
        self.c.bind("<B2-Motion>", self.rotate)
        
        self.root.bind("<MouseWheel>", self.zoom)        

    def zoom(self, event):
        'зуминг сцены'
        self._zoom -= event.delta/120.0
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

    def rotate(self, event):
        'вращение сцены'
        dx = event.x - self.last_x
        dy = event.y - self.last_y

        self.rot_x += dy
        self.rot_y -= dx

        self.draw()
        self.last_x = event.x
        self.last_y = event.y

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

        #TODO: рисуем стол
        table = [
            Point_v(0, 0, 0, 'yellow'),
            Point_v(0, 0, 100, 'yellow'),
            Point_v(0, 0, 0, 'yellow'),
            Point_v(0, 0, 0, 'yellow'),
        ]

        #проходим по всем точкам без учета цвета и вычисляем смещение для центрирование на сцене
        xx = []
        yy = []
        zz = []
        for i in self.points:
            xx.append(i.X)
            yy.append(i.Y)
            zz.append(i.Z)
        minx = min(xx)
        maxx = max(xx)
        
        self.shift_x = (maxx + minx)/2 - minx

        miny = min(yy)
        maxy = max(yy)
        self.shift_y = (maxy + miny)/2 - miny

        minz = min(zz)
        maxz = max(zz)
        self.shift_z = (maxz + minz)/2 - minz

        p = [] #тут будут наши спроецированные точки
        #преобразуем наши точки в 2D
        curr_type = None

        for i in self.points:
            tmp = self.to_2D(i)
            if( curr_type == None ):
                curr_type = i.Type
            if( i.Type != curr_type ): #сменился тип, рисуем накопленные линии
                self.c.create_line(p, tags="theline", fill=curr_type)
                curr_type = i.Type
                p = p[-2:] #оставляем последнюю точку

            #добавляем во временный массив
            p.append(tmp.X)
            p.append(tmp.Y)

        #рисуем оставшиеся линии
        self.c.create_line(p, tags="theline", fill=curr_type)
        #print self._zoom	

    def to_2D(self, p):
        x = p.X - self.shift_x # + self.scroll_x
        y = p.Y - self.shift_y# + self.scroll_y
        z = (p.Z - self.shift_z)/(self._zoom/10.)
        

        t = Point_v(x, -y, p.Z, p.Type)

        a_x = self.rot_x/100.
        a_y = self.rot_y/100.

        tmp = t.rot_x(a_x)
        tmp = tmp.rot_y(a_y)

#		print "zoom: ", self._zoom, "a_x: ", self.rot_x, "a_y: ", self.rot_y
        zzz = 300		

        sx = self.size_x/2 + tmp.X*zzz/(tmp.Z + zzz)/(self._zoom/300.)
        sy = self.size_y/2 + tmp.Y*zzz/(tmp.Z + zzz)/(self._zoom/300.)

        sx += self.scroll_x
        sy += self.scroll_y
        return Point_v(sx, sy, 0, p.Type)

def go_home():
    from main import G0
    G0(X=0, Y=0, Z=0)

def f():
    from main import G1
    go_home()
    G1(Z=10)
    G1(X=50)
    G1(Y=30)
    G1(X=0)
    G1(Y=0)
    G1(Z=0)
    go_home()

#export(f, 'test.nc')

if __name__ == '__main__':
    Viewer3D(f).show()
