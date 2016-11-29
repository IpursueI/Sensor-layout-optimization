#-*- coding:utf-8 -*-

#from __future__ import print_function
import math
import random
from simanneal import Annealer
import sys
sys.path.append("..")
from pick_tactics.tactics import PickTactics
from accuracy.root_mean_square_error import RMSE
from interpolation.ordinary_kriging import OrdinaryKriging

class LayoutOptimization(Annealer):

    """模拟退火对传感器布局进行优化
    """
    
    def __init__(self, choice, sensors, total_number, selected_number):
        self.sensors = sensors
        self.total_number = total_number
        self.selected_number = selected_number
        super(LayoutOptimization, self).__init__(choice)  # important! 

    def move(self):
        a = random.choice(self.choice)
        unselected = list(set(range(self.total_number)).difference(set(choice)))
        b = random.choice(unselected)
        self.choice.remove(a)
        self.choice.append(b)

    def energy(self):
        e = 0
        for i in range(len(self.state)):
            e += self.distance_matrix[self.state[i-1]][self.state[i]]
        return e


if __name__ == '__main__':
    print "aa"