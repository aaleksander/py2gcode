# -*- coding: utf-8 -*-

from main import *
from math import sqrt

def get_xx_yy_len(p1,  p2):    
    x1 = p1['x']
    y1 = p1['y']
    x2 = p2['x']
    y2 = p2['y']
    l = sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))     
    return (x1,  y1,  x2,  y2,  l)
    
def get_len(p1,  p2):
    x1,  y1,  x2,  y2,  l = get_xx_yy_len(p1,  p2)
    return l

class Trajectory(object):
    def __init__(self):
        self.points = [] #это уже готовые точки, по которым пойдет фреза. Словарик вида {x, y}
        self.jump_points = []

    def get_first_position(self):
        'получить первую точку траектории'
        if len(self.points) == 0:
            self.create_trajectory()
        if len(self.points) == 0:
            raise Exception("Метод create_trajectory не переопределен")
        p = self.points[0]
        return p['x'],  p['y']

    def create_trajectory(self):
        'создает траекторию,  потом обязательно вызвать update_offsets'
        pass
        
    def create_path(self):
        'рисует путь,  как он есть'
        pass

    def draw_points(self,  canvas):
        'рисует опорные точки'
        pass

    def to_gcode(self, z = None,  z_up=None):
        'отправляем все в Г-код. Режем на глубине z, на перемычках поднимаемся до z_up'
        if len(self.jump_points) > 0 and z_up == None:
            raise Exception("Не задана вторая Z-координата для траектории с перемычками")

        G1(Z=z)
        self.create_trajectory()
        
        if len(self.jump_points) == 0:  #плоская траектория, без всяких перемычек
            for p in self.points:
                G1(p['x'],  p['y'])
        else: #код с учетом перемычек
            curr_z = z
            for p in self.__get_next_point():                
                if p['type'] == 'f':
                    if curr_z != z: #чтобы бесконечно не гонять G1 Z
                        G1(Z = z)
                        curr_z = z
                    G1(X=p['x'],  Y=p['y'])
                else:
                    if z < z_up:
                        if curr_z != z_up:
                            G1(Z = z_up)
                            curr_z = z_up
                    G1(X=p['x'],  Y=p['y'])

    def jump_point(self, w, offs):
        '''добавить перемычки
            w - ширина перемычек в мм
            offs - массив смещений в процентах, относительно общей длины траектории
            z - от какой глубины начать, т.е. если =-18, то ниже этой глубины фреза в этом месте не опустится, а поднимется до -18 и пройдет это место, потому опять опустится, где была
        '''
        l = self.length() #общая длина
        #переводим процентные величины в конкретную дистанцию на траектории начала и конца перемычки
        for i in offs:
            start = l/100.*i - w/2.0
            stop = l/100.*i + w/2.
            if start >= 0: 
                self.jump_points.append({'w': w,  'start': start,  'stop': stop})
            else: #перемычка "переваливает" через нулевую отметку
                self.jump_points.append({'w': w,  'start': 0,  'stop': stop})
                self.jump_points.append({'w': w,  'start': l + start,  'stop': 0})

        self.update_offsets()


    def __get_next_point(self):
        'возвращает точки по одной с указанием типа (перемычка или просто подача) '
        #объединяем перемычки и точки
        #уберем из траектории отрезки повторяющейся длины
        prev = self.points[0]
        tmp = [prev]        
        for p in self.points[1:]:
            len = get_len(prev,  p)
                
            if len != 0:
                tmp.append(p)
            prev = p
        self.points = tmp
        
        #сделаем из перемычек, список точек
        jp = []
        for j in self.jump_points:
            jp.append({'x': None,  'y': None,  'off': j['start'],  'type': 'start'})#,  '_____*****_____':1})
            jp.append({'x': None,  'y': None,  'off': j['stop'],  'type': 'stop'})#,  '_____*****_____':1})
        list = self.points + jp        
        
        list = sorted(list,  lambda a,  b: 1 if a['off'] > b['off'] else -1) #сортируем по возрастанию off
        type = None
        for p in list:
            if 'type' in p.keys():
                if p['type'] == 'start':
                    type = 'between'
                if p['type'] == 'stop':
                    type = None
                continue
            else:              
                if type != None:
                    p['type'] = type
                  
       
                
        def get_point(start): # найти ближайшую точку-не-перемычку (идя вперед)
            i = 0
            for p in list:
                if i < start:
                    i += 1
                    continue
                if not 'type' in p.keys() or p['type'] == 'between':
                    return p
                i += 1
            return None
            
        prev = list[0] #предыдущая найденная точка
        i = 0
        for p in list[1:]:
            if 'type' in p.keys(): #перемычка
                next = get_point(i + 1)
                x1,  y1,  x2,  y2,  len = get_xx_yy_len(prev,  next)

                o = p['off'] - prev['off']
                if o == 0 or len == 0:
                    continue
                do = len/o                
                
                x = x1 + (x2 - x1)/do
                y = y1 + (y2 - y1)/do
                p['x'] = x
                p['y'] = y
                
            prev = p
            i += 1
        
        for p in list:
            if 'type' in p.keys() and p['type'] in ['stop',  'between']:
                yield {'type': 'j',  'x': p['x'],  'y': p['y']}
            else:
                yield {'type': 'f',  'x': p['x'],  'y': p['y']}

    def update_offsets(self):
         #дополним каждую точку смещением, чтобы легче было считать перемычки
        prev = self.points[0]
        prev['off'] = 0
        off=0
        for p in self.points[1:]:
            len = get_len(prev,  p) #длина нового отрезка
            off += len
            p['off'] = off

            prev = p

    def __in_jump_point(self,  offset):
        'возвращает (None, None), если не попали в перемычку, иначе (start, stop) перемычки'
        for p in self.jump_points:
            if offset >= p['start'] and offset <= p['stop']: #попали внутрь перемычки
                return (p['start'],  p['stop'])
                
        return (None,  None)

    def length(self):
        'возвращает длину траетории'
        if len(self.points) == 0:
            self.create_trajectory()

        res = 0
        prev = self.points[0]
        for p in self.points[1:]:
            res += get_len(prev,  p)
            prev = p

        return res

    def show(self, scale = 1):
        'предварительный просмотр траектории'
        self.root = Tk()

        self.root.title("MetaViewer")
        self.canvas = Canvas(self.root, bg="white", width=640, height=480)
        self.canvas.configure(background='black', width=1000, height=600)
        self.canvas.pack()
        self.canvas.delete('all')

        self.draw_points(self.canvas) #рисуем опорные точки

        #расчитаем траекторию и перемычки
        self.create_trajectory()
        

        #рисуем
        prev = None
        for p in self.__get_next_point():
            if prev == None:
                prev = p
                continue
            if p['type'] == 'f': #подача
                col = 'red'
                w = 2
            else:  #перемычка
                col = 'green' 
                w = 5
            self.canvas.create_line(prev['x'],  prev['y'],  p['x'],  p['y'],  fill=col,  width=w) 
            prev = p

        self.canvas.scale("all",  0,  0,  scale,   scale)
        #главный цикл приложения
        self.root.mainloop()

    def draw(self,  canvas,  scr_x, scr_y,  scale):
        self.draw_points(canvas,  scr_x,  scr_y,  scale) #рисуем опорные точки
        #расчитаем траекторию и перемычки
        self.create_trajectory()
        #рисуем
        prev = None
        for p in self.__get_next_point():
            if p['x'] == None:
                continue
            if prev == None:
                prev = p
                continue
            if p['type'] == 'f': #подача
                col = 'red'
                w = 2
            else:  #перемычка
                col = 'green' 
                w = 5
            canvas.create_line(prev['x']*scale + scr_x,  
                               prev['y']*scale + scr_y,  
                               p['x']*scale + scr_x,  
                               p['y']*scale + scr_y,  fill=col,  width=w) 
            prev = p


if __name__ == '__main__':
    from meta import *
    v = Meta()

    v.point(0, 0,  rounding=5)
    v.point(50, 0,  rounding=5)
    v.point(50, 20)
    v.point(40, 30)
    v.point(50, 100,  rounding=5)    
    v.point(0, 100,  rounding=5) 
    v.point(-50,  50,  radius=-60)        


#TODO: добавить возможность ставить перемычку на 0
    #v.jump_point(5, [10,  38,  70,  95]) #перемычки, толщиной 5 мм
#    v.jump_point(5, [10,  38,  70,  95]) #перемычки, толщиной 5 мм

    preview2D([v],  4)

#    v.show(10) #показать плоскую траекторию в 10х кратном увеличении

    def f():
        F(300)
        G0(0, 0, 5)
        F(1000)
        x,  y =  v.get_first_position()
        G0(x, y)

        z = -3
        while z > -10:            
            v.to_gcode(z,  -7.5)
            z -= 1
        G0(Z=5)

#    preview(f)
    #export(f)
