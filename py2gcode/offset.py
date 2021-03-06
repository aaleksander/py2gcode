# -*- coding: utf-8 -*-
#Стратегия, которая расчитывает offset для сложных фигур
#алгоритм тупой до безобразия: по всей траектории создаем маленькие точки с заданным шагом. И на каждом шаге "рисуем" окружность-фрезу, и по этим окружностям строим касательные
#Как бы маленькими шажочками
from svg import *
from main import *
from trajectory import *
from tool import *
from meta import *
from clipper import *

default_safeZ = 5



class Offset(Meta):
    def __init__(self, t, offset, limit=0.05):#, x_start, y_start):
        super(Offset,  self).__init__()
        self.offset = offset
        self.src = t #начальная траектория

        #создаем мета-траекторию
        if len(self.src.points) == 0:
            self.src.create_trajectory()

        #удалим отрезки нулевой длины
        prev = t.points[0]
        tmp = [prev]        
        for p in t.points[1:]:
            len2 = get_len(prev,  p)

            if len2 != 0:
                tmp.append(p)
            prev = p
        t.points = tmp

        min_len = limit #минимальная длина отрезка, ради которой стОи что-то считать
        i = 0
        first_prev = None

        while i < len(t.points):
            s = Point(t.points[i]['x'], t.points[i]['y'])

            s_prev = get_from_ring(t.points, i, -1, to_point)
            i_prev = -1
            while dist(s, s_prev) < min_len:
                i_prev -= 1
                s_prev = get_from_ring(t.points, i, i_prev, to_point)

            if s_prev == first_prev: #контур замкнулся, выходим
                break            

            if first_prev == None: #запомним первую точку
                first_prev = s_prev

            s_past = get_from_ring(t.points, i, 1, to_point)
            i_past = 1
            while dist(s, s_past) < min_len:
                i_past += 1
                s_past = get_from_ring(t.points, i, i_past, to_point)

            i_past = i_past + i

            zero = Point(s.x + 100, s.y)
            a = get_angle(s_prev, s, s, s_past)
            aa = a*180.0/3.14159265358979323

            if offset > 0: #обводим снаружи
                if aa > 180: #внутренний угол
                    self.point(s.x, s.y, radius=-self.offset)            
                else:
                    pp1 = get_border(s_prev, s, self.offset)
                    pp2 = get_border(s, s_past, self.offset)
                    pp = get_cross_point(pp1[0], pp1[1], pp2[0], pp2[1])
                    self.point(pp.x, pp.y)
            else:
                if aa < 180: #внутренний угол
                    self.point(s.x, s.y, radius=-self.offset)            
                else:
                    pp1 = get_border(s_prev, s, self.offset)
                    pp2 = get_border(s, s_past, self.offset)
                    pp = get_cross_point(pp1[0], pp1[1], pp2[0], pp2[1])
                    self.point(pp.x, pp.y)

            i = i_past
        self.__uncross()

    def __uncross(self):
        'убирает пересечения контура'
        '''
        if len(self.points) == 0:
            self.create_trajectory()

        s = []
        for p in self.points:
            s.append(Point(p['x'], p['y']))

        or_src = self.orientation() #изначальная ориентация
        print or_src
        res = SimplifyPolygons([s], PolyFillType.NonZero)
        if len(res) == 1: #полигон не самопересекающийся
            return

        tt = []
        for r in res:
            t = Trajectory()
            for p in r:
                t.points.append({'x': p.x, 'y': p.y})
            tt.append(t)

        tt = sorted(tt, key=lambda x: abs(x.orientation()))
        tt.reverse()
        
        self.points = tt[0].points
        self.points.insert(0, self.points[len(self.points) - 1].copy())
        
        if self.src.orientation() > 0 and self.orientation() < 0:
            self.points.reverse()
            
        self.update_offsets()'''

        #ищем пересекающиеся сегменты        
        newp = []
        for p11, p12 in self.segments(to_point):
            for p21, p22 in self.segments(to_point):
                if p11.x == p21.x and p12.x == p22.x and p11.y == p21.y and p12.y == p22.y: #совпадают                    
                    continue
                if (p12.x == p21.x and p12.y == p21.y) or (p22.x == p11.x and p22.y == p11.y): #совпадают
                    continue

                if is_cross(p11, p12, p21, p22):
                    #пересекается, внедряем новую точку
                    p = get_cross_point(p11, p12, p21, p22)

                    #newp.append({'x': p.x, 'y': p.y, 'off': 0, 'after':  (p11, p21)})
                else:
                    pass
        #self.points += newp


'''
from clipper import *
class Offset(Trajectory):
    'на основе clipperа делает оффсет полигона'
    def __init__(self, tr, offset):
        super(Offset,  self).__init__()

        self.src = tr #начальная траектория
        #создаем мета-траекторию
        if len(self.src.points) == 0:
            self.src.create_trajectory()

        s = []
        for p in tr.points:
            s.append(Point(p['x'], p['y']))
        #s = [Point(10,10),Point(30,30), Point(20,80), 
        #    Point(40,80), Point(40,50), Point(80,50), Point(70,30), Point(80,10)]

        subj = []
        subj.append(s)
        clip = OffsetPolygons(subj, offset, JoinType.Round)

        #превращаем обратно в словарики
        self.points = []
        for p in clip[0]:
            self.points.append({'x': p.x, 'y': p.y, 'off': 0})
        self.points.append({'x': clip[0][0].x, 'y': clip[0][0].y, 'off': 0})'''

if __name__ == '__main__':
    #str = 'm 26.375797,-199.69209 c -0.743175,5.1898 -0.605986,14.11446 3.500577,21.48348 4.106564,7.36901 17.023812,14.92751 28.541993,15.00196 11.518181,0.0744 22.231005,-4.04074 29.080635,-2.69265 6.84963,1.34809 16.841128,12.84577 18.558968,17.93726 -2.65497,6.15181 -11.378568,5.75807 -16.404848,8.71999 -1.4269,1.06002 -3.57527,3.37468 -1.34632,6.46236 1.93668,2.85864 23.188378,-5.06676 32.581098,9.96282 3.45557,5.7892 10.71316,14.66647 7.53942,16.96371 0.0224,0.86389 -6.82138,0.71804 -10.23207,1.07706 -1.77208,0.1876 -1.64017,3.23118 0.53853,4.846773 12.61059,10.50134 18.75881,31.90793 17.23297,56.5457 -2.05596,19.722015 -10.49029,36.4929249 -20.73342,36.8893249 -10.00654,0.7809 -16.966678,-3.6740999 -18.310048,-15.0788399 -0.58769,-3.85122 -1.14271,-14.22222 10.232078,-16.694445 9.7685,-1.38635 11.93706,8.797745 11.57842,12.386205 -0.35864,3.58846 -3.6634,6.29488 -7.8441,8.20238 -0.8119,0.3704 -2.20829,2.0247 -0.7724,3.0731 2.78485,1.7165 7.3142,1.5848 12.38621,-3.4668 5.07201,-5.0515 4.39464,-19.380775 -0.8078,-30.696235 -3.84313,-8.92387 -10.35187,-21.46531 -12.38621,-24.7724 -2.48047,-4.2132 -7.35742,-5.3902 -9.15501,-3.50045 -1.797588,1.88975 -0.167968,7.199836 2.24932,11.20322 2.41729,4.003384 4.99278,14.612385 3.39311,18.207399 -0.34159,0.767664 -1.10159,1.283243 -1.60346,1.285621 -4.936528,0.56097 -18.382368,-1.80194 -21.339258,-10.50135 -2.95689,-8.69941 -1.91348,-14.31521 -3.7024,-20.93537 -1.78893,-6.62015 -8.36683,-8.17514 -9.5589,-0.87511 -1.192081,7.30004 7.596269,20.456037 2.01947,21.27195 -6.013585,0.8078 -21.075935,-9.52751 -31.773285,-29.88843 -10.69735,-20.360923 -29.090241,-65.127113 -25.04167,-103.397843 1.92432,-15.39344 6.69801,-22.59508 13.86716,-28.67675 7.16915,-6.08167 17.77657,-5.78507 26.99582,-1.08664 9.21926,4.69843 14.597105,21.82148 10.29741,28.9556 -4.29968,7.13411 -8.07989,8.48157 -14.67495,7.53942 -6.59505,-0.94215 -10.66933,-7.31307 -9.82818,-13.73252 0.84115,-6.41945 5.84214,-9.02168 9.42428,-8.88576 3.58214,0.13592 4.35313,1.14438 5.58726,2.08681 1.936175,1.20701 2.890072,-1.0983 2.121922,-2.43546 -2.461025,-4.284 -5.07646,-7.08811 -11.209632,-8.26784 -6.133172,-1.17972 -13.003144,1.59443 -15.75201,4.57751 -2.748866,2.98308 -4.507505,5.71544 -5.25068,10.90524 z'
    #str = 'm 8.5518444,-108.92843 c 1.4948896,20.161912 5.2547266,45.118986 30.9392166,61.960266 25.684484,16.84128 37.732634,21.36533 42.449184,29.50532 4.716538,8.1399835 2.0527,16.2264435 -8.34722,14.2710535 C 63.193105,-5.1471805 37.331975,-18.147884 21.542272,-45.093024 5.7525688,-72.038154 4.4283794,-104.03584 5.3450277,-108.74695 c 0.3416653,-2.26348 3.0669059,-2.02972 3.2068167,-0.18148 z'
    #str = 'M 8.1026786,4.5273595 C 23.281251,3.8428357 34.904014,5.0978624 50.357143,10.665752 c 15.45313,5.567891 26.474514,15.423018 35.714286,23.482143 9.239772,8.059125 15.513801,15.026289 23.853551,22.159261 1.61621,1.271403 3.26411,-0.533279 2.57046,-1.885934 -3.33333,-5.833333 -4.17877,-10.296224 -2.22758,-17.773327 1.95119,-7.477102 9.00252,-16.375976 16.51785,-21.071428 7.51533,-4.695452 19.30906,-8.7672524 40.80358,-10.5357146 21.49452,-1.7684622 35.74128,0.736352 56.51785,3.3035714 C 244.8837,10.911543 267.13649,19.576437 290,20.755039 c 22.8635,1.178601 26.2536,-2.491903 35.8667,-5.289522 1.72258,-0.337284 2.68847,1.694676 1.45024,2.821088 -6.99405,6.309524 -16.3258,13.577255 -29.99551,15.236291 -13.66972,1.659036 -27.55282,-4.544034 -38.39286,-9.017858 -10.84004,-4.473824 -14.39732,-5.565476 -22.61161,-8.660714 -2.20238,-0.833334 -3.48958,2.061012 -0.95982,2.946429 10.11905,3.869048 19.09102,6.784966 25.71429,12.232143 6.62327,5.447176 11.30378,11.478244 11.33928,19.642856 0.0355,8.164612 -8.17679,12.189382 -14.55357,12.410715 -6.37678,0.221333 -10.57447,-2.795636 -12.95127,-5.083673 -0.67114,-0.646072 -1.27205,-0.983299 -1.06658,-2.505613 -0.11905,-15.535714 -1.29506,-16.371358 -5.35715,-23.035715 -4.06208,-6.664357 -10.78125,-10.669642 -18.63839,-15.044642 -1.48065,-1.078869 -3.34077,1.101191 -1.94196,2.544643 3.57143,3.095238 6.29256,3.363018 12.54464,10.714285 6.25207,7.351267 8.22489,14.688851 6.69643,22.678572 -1.52847,7.989721 -10.18305,15.42025 -17.32143,16.607143 -7.13838,1.186892 -13.28535,-2.563318 -14.01785,-6.160715 -0.73251,-3.597397 1.1322,-5.010073 6.24999,-8.749999 5.11779,-3.739926 8.93038,-13.826639 5.35715,-21.875001 -3.57324,-8.048362 -5.37809,-8.860227 -9.91072,-12.499999 -4.53263,-3.639772 -4.79167,-4.017858 -7.23214,-5.267858 -1.77827,-0.818453 -3.69048,1.39881 -1.69643,3.035714 3.57143,3.452381 11.1588,7.923136 12.86085,13.618475 1.70206,5.695338 1.23781,11.557546 -2.81753,17.873232 -4.05533,6.315685 -17.15368,12.33773 -23.64013,14.224438 -6.48645,1.886708 -23.44636,0.508993 -27.11748,-0.716144 -3.67112,-1.225137 -5.32314,-1.799084 -6.46186,-2.474338 -1.81692,-1.077429 -0.75439,-3.203965 0.70994,-3.053717 12.24702,0.505953 24.56145,-0.707065 28.92157,-2.686231 4.36012,-1.979167 11.17548,-5.83498 14.64602,-12.608322 3.47054,-6.773342 1.56382,-12.874984 0.083,-15.878308 -1.48088,-3.003324 -5.19838,-7.293525 -8.79148,-9.63837 -1.9355,-1.131059 -3.43487,1.496631 -1.79337,2.843138 4.928,4.82318 8.58413,11.568368 5.68945,18.855149 -2.89469,7.286781 -10.92438,11.820985 -18.25576,13.591234 -7.33138,1.770249 -18.50637,1.308017 -24.43364,-1.976976 -5.92728,-3.284994 -7.32646,-7.557992 -5.77742,-12.368155 1.54904,-4.810163 8.21406,-7.110793 14.3379,-7.570681 1.46747,0.159144 1.76832,1.380586 1.50685,2.36062 -0.40958,1.53515 1.86293,3.617779 5.45941,4.345983 3.59648,0.728204 17.40659,2.151287 17.16266,-8.997281 -0.24393,-11.148568 -19.46859,-13.135858 -30.55584,-11.336339 -11.08725,1.799519 -25.59868,9.983252 -28.08058,23.302802 -2.4819,13.319549 5.83384,23.328319 23.49035,31.86122 17.65651,8.532901 45.94571,13.06318 74.0178,9.017857 28.07209,-4.045323 63.40556,-17.836732 88.83928,-32.410714 25.43372,-14.573982 43.89037,-26.721172 64.64287,-34.107143 20.7525,-7.3859712 33.06547,-9.4575893 42.67857,-10.1785714 9.61309,-0.720982 16.71558,0.6352052 24.33463,1.3494909 2.01668,0.094359 1.80794,3.1976396 -0.18422,3.1562465 -22.08333,-0.6845236 -48.19067,8.69774 -63.97184,16.744263 -15.78117,8.046523 -25.55009,20.90815 -24.73215,33.75 0.81795,12.84185 15.51967,20.083051 28.30358,22.321428 12.78391,2.238377 27.93872,-1.348465 37.23214,-6.964285 9.29342,-5.61582 6.4667,-16.287596 -1.875,-21.25 -8.3417,-4.962404 -14.85661,-3.290058 -22.23756,-2.784105 -2.14286,0.357142 -1.7803,3.173744 0.26244,3.257148 2.24989,0.261925 1.94576,4.054714 -0.25703,6.044814 -2.20278,1.990101 -5.36997,3.657896 -9.73214,3.214285 -4.36217,-0.44361 -10.1122,-2.911108 -9.55357,-8.124999 0.55863,-5.213892 6.2594,-8.668033 13.39286,-10.625001 7.13346,-1.956968 19.23034,-1.841572 27.41258,0.594362 8.18224,2.435934 15.62754,6.391358 18.56956,13.423496 2.94202,7.032138 2.83293,15.080713 -6.19956,21.260832 C 417.6251,85.87456 403.97214,91.248117 386.05162,90.428534 368.1311,89.60895 355.32475,83.195621 348.82583,78.327146 342.3269,73.458671 337.48019,62.701376 337.859,56.180572 c 0.3788,-6.520805 7.31648,-14.356892 7.31648,-14.356892 1.46385,-2.042793 -0.62711,-3.673558 -2.1947,-2.566693 -1.12565,0.91746 -40.74723,24.422558 -59.32007,32.390908 -18.57284,7.96835 -33.99195,12.8347 -52.58928,15.714286 -18.59733,2.879586 -39.59005,4.112915 -58.66071,1.517857 -19.07067,-2.595059 -44.35697,-10.267064 -59.28572,-20 C 98.196261,59.147102 76.237602,39.734011 62.589286,28.344324 48.94097,16.954637 23.57887,7.7342047 8.1919643,7.7639667 5.8686537,7.7230296 6.1588616,4.4817464 8.1026786,4.5273595 z'
    #m = SvgTrajectory(str)
    #t.to_zero()

    m = Meta()
    m.point(10,  0)
    m.point(0, 10)
    m.point(0, 50)
    #m.point(40, 50)
    #m.point(40, 70)
    #m.point(60, 70)
    #m.point(60, 50)
    m.point(100, 50)#, rounding=10)
    m.point(100, 0)

    offset = -4
    o = Offset(m, offset)
    l = [m, o]
    for i in xrange(0, 4):
        o = Offset(o, offset)
        l += [o]

    preview2D(l, 10, options={'hideRef': True})

    def f():
        G0(0, 0, 5)

        o = Offset(m, -3)
        for i in xrange(0, 10):
            mill_offset(o, -1.5, z_start=-1, z_stop=-5, z_step=3, options={'x': 0, 'y': 0, 'z': -10, 'angle':1})
        G0(Z=5)

    #preview(f)
    #export(f)
