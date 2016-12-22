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
from draw.draw_layout import drawLayout

class LayoutOptimization(Annealer):

    """模拟退火对传感器布局进行优化
    """
    
    def __init__(self, state, total_number,filtered_file_path, pos_file_path, each_sensor_number):
        self.total_number = total_number
        self.filtered_file_path = filtered_file_path
        self.each_sensor_number = each_sensor_number
        self.pos_file_path = pos_file_path
        self.sensor_num = ['10728412','10728515','10728382','10728506','10728402','10728400','10728435','10728517','10728383',
        '10728534','10728432','10728401','10728391','10728437','10728525','10728399','10728518','10728442','10728527','10728390',
        '10728405','10728419','10728425','10728439','10728404','10728408','10728522','10728396','10728422','10728507','10728513',
        '10728387','10728385','10728519']
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
        ok3d = OrdinaryKriging(self.filtered_file_path, self.pos_file_path, selected_sensors,unselected_sensors, self.each_sensor_number, 'linear')
        rmse = RMSE(ok3d.run())
        #print(self.state)
        #return rmse.temperature_error()
        return rmse.humidity_error()


if __name__ == '__main__':
    #state = random.sample(range(34), 6)
    state = [1,2,3,4,5]
    lay_opt = LayoutOptimization(state, 34, "../data/filter_data","../data/pos/pos.csv", 10)
    lay_opt.copy_strategy = "slice"
    lay_opt.steps = 10000
    lay_opt.updates = 1000
    state, e = lay_opt.anneal()
    state = sorted(state)
    print("root_mean_square_error: %f" % e)
    print("final state: ", state)
    print("-----end-----")
    sensors = [lay_opt.sensor_num[item] for item in state]
    sensors.append(str(e))
    print("sensors:", sensors)

    #对传感器的布局进行绘制
    drawer = drawLayout('../data/pos/pos.csv','../draw/sensor.png',sensors)
    drawer.main()