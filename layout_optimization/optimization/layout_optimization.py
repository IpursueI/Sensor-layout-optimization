#-*- coding:utf-8 -*-

from __future__ import print_function
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
    
    def __init__(self, state, total_number,filtered_file_path, pos_file_path, each_sensor_number):
        self.total_number = total_number
        self.filtered_file_path = filtered_file_path
        self.each_sensor_number = each_sensor_number
        self.pos_file_path = pos_file_path
        super(LayoutOptimization, self).__init__(state)  # important! 

    def move(self):
        a = random.choice(self.state)
        unselected = list(set(range(self.total_number)).difference(set(self.state)))
        b = random.choice(unselected)
        self.state.remove(a)
        self.state.append(b)
        #print("state: ",self.state)

    def energy(self):
        tac = PickTactics()
        selected_sensors,unselected_sensors = tac.fixed_tactic(self.state)
        ok3d = OrdinaryKriging(self.filtered_file_path, self.pos_file_path, selected_sensors,unselected_sensors, self.each_sensor_number)
        rmse = RMSE(ok3d.run())
        #print(self.state)
        return rmse.temperature_error()


if __name__ == '__main__':
    #state = random.sample(range(34), 6)
    state = [1,2,3,4,5,6]
    lay_opt = LayoutOptimization(state, 34, "../data/filter_data","../data/pos/pos.csv", 2)
    lay_opt.copy_strategy = "slice"
    lay_opt.steps = 300
    lay_opt.updates = 300
    state, e = lay_opt.anneal()
    print("root_mean_square_error: %f" % e)
    print("final state: ", state)
    print("-----end-----")