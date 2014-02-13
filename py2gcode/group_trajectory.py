# -*- coding: utf-8 -*-

from main import *


#класс рулит целой группой траекторий. Удобно для гравировки текста

class GroupTrajectory(object):
    def __init__(self):
        self.trajectories = []

    def add_svg(self, str):
        'берет траектории из строки svg'
        paths = str.split('z')
        paths = map(strip, paths)
        for p in paths:
            self.trajectories.append(Svg(p))

    def get_next_trajectory(self):
        'выдает траектории по одной'
        for t in self.trajectories :
            yield t

