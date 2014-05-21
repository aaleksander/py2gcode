#-*- coding: utf-8 -*-
import math

from geometry import *

def _get_cross_segment(points, i1, i2):
    '''возвращает пару индексов-вершин для линии, которая пересекает линию из вершин points[i1]-points[i2]
    Причем, эта линия самая последняя в списке
    '''
    p1, p2 = points[i1], points[i2]
    tail = points[i2 + 1:] #берем хвостик и переворачиваем
    tail.reverse()
    prev = tail[0]
    i = len(points) - 1
    for p in tail:
        if is_cross(p1, p2, prev, p):
            return i, i + 1
        prev = p
        i -= 1
    
    return None, None    

def simple_polygon(points):
    'получает на вход список точек (словарики x, y) и возвращает список полигонов (список списков словариков)'
    return [points]

def isSimple(points):
    'возвращает истину, если полигон не пересекает сам себя'    
    p1 = to_point(points[0])
    for p2 in map(to_point, points[1:] + [points[0]]): #полигон замыкаем в кольцо
        p3 = to_point(points[0])        
        for p4 in map(to_point, points[1:] + [points[0]]): #полигон замыкаем в кольцо
            if p1 == p3 or p2== p4 or p1 == p4 or p2 == p3: #совпадают
                p3 = p4
                continue
            if is_cross(p1, p2, p3, p4):
                return False
            p3 = p4
        p1 = p2
    return True    
    
#ТЕСТЫ    
    
import unittest

def p(x, y):
    'создает словарик'
    return {'x': x, 'y': y}
    
def pp(arr):
    'создает массив словариков из массива кортежей'
    res = []
    for x, y in arr:
        res.append(p(x, y))
    return res


simplePolygon = pp([(0, 0), (0, 10), (10, 10), (10, 0)]) #простой непересекающийся полигон
oneCrossPolygon = pp([(0, 0), (0, 10), (10, 0), (10, 10)]) #полигон с одним пересечением
crossPolygon=pp([(0, 0), (0, 10), (20, 0), (30, 10), (30, 0)]) #полигон, где вершина лежит на ребре

class TestCliper(unittest.TestCase):    
    def test_issimple(self):        
        #self.assertTrue(isSimple(simplePolygon), "Неправильно определил простой полигон")
        self.assertFalse(isSimple(oneCrossPolygon), "Неправильно определил пересекающийся полигон")
        #self.assertFalse(isSimple(crossPolygon), "Неправильно определил полигон с вершиной на ребре")

    def test_simple_polygon(self):
        self.assertTrue(len(simple_polygon(simplePolygon)) == 1, 'Количество вернувшихся полигонов для простого полигона неверно')
        self.assertTrue(simple_polygon(simple_polygon)[0] == simple_polygon, 'вернули не тот полигон')
        

    def _test_oneCrossPolygon(self):
        res = simple_polygon(oneCrossPolygon)
        self.assertTrue(len(res) == 2, 'Количество вернувшихся полигонов для сложного полигона неверно')        

    def test_getCrossSegment(self):
        p1, p2 = _get_cross_segment(simplePolygon, 0, 1)
        self.assertTrue(p1 == None)
        self.assertTrue(p2 == None)
        
        p1, p2 = _get_cross_segment(oneCrossPolygon, 0, 1)
        self.assertTrue(p1 == 2, 'индекс неверный')
        self.assertTrue(p2 == 0, 'индекс неверный')
        

if __name__ == '__main__':
    unittest.main()
