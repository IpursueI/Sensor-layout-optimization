#-*- coding:utf-8 -*-

#from __future__ import print_function
import math
import random
#from simanneal import Annealer
import csv
import sys
sys.path.append("..")
from simanneal.anneal import Annealer
from pick_tactics.tactics import PickTactics
from accuracy.root_mean_square_error import RMSE
from interpolation.ordinary_kriging import OrdinaryKriging
from draw.draw_layout import drawLayout

class LayoutOptimization(Annealer):

    """模拟退火对传感器布局进行优化
    """
    
    def __init__(self, state, total_number,filtered_file_path, pos_file_path, each_sensor_number, goal):
        self.total_number = total_number
        self.filtered_file_path = filtered_file_path
        self.each_sensor_number = each_sensor_number
        self.pos_file_path = pos_file_path
        self.goal = goal
        self.sensor_num = ['10728412','10728515','10728382','10728506','10728402','10728400','10728435','10728517','10728383',
        '10728534','10728432','10728401','10728391','10728437','10728525','10728399','10728518','10728442','10728527','10728390',
        '10728405','10728419','10728425','10728439','10728404','10728408','10728522','10728396','10728422','10728507','10728513',
        '10728387','10728385','10728519']

        super(LayoutOptimization, self).__init__(state)  # important! 

    def set_sensor_weight(self):
        #这几个传感器的权重为2，其余传感器的权重为1
        weight = {2:set(['10728399', '10728518', '10728442', '10728527', '10728390', '10728405', '10728419', '10728425', '10728439', '10728404', 
                    '10728513', '10728387', '10728385', '10728519'])}

        self.sensor_weight = {}
        for item in self.sensor_num:
            self.sensor_weight[item] = 1
        
        for item in weight:
            for sensor in weight[item]:
                self.sensor_weight[sensor] = item

    def weight_select(self, unselected):
        pos = [0]
        start = 0
        for item in unselected:
            start += self.sensor_weight[item]
            pos.append(start)

        res = random.choice(range(1,start+1))
        final = 1
        for i in range(1,len(pos)):
            if res>pos[i-1] and res<=pos[i]:
                final = i
                break
        return unselected[final-1]

    def move(self):
        a = random.choice(self.state)
        unselected = list(set(range(self.total_number)).difference(set(self.state)))
        b = self.weight_select(unselected)
        self.state.remove(a)
        self.state.append(b)
        #print("state: ",self.state)

    def energy(self):
        tac = PickTactics()
        selected_sensors,unselected_sensors = tac.fixed_tactic(self.state)
        ok3d = OrdinaryKriging(self.filtered_file_path, self.pos_file_path, selected_sensors,unselected_sensors, self.each_sensor_number, 0, 'linear')
        rmse = RMSE(ok3d.run())
        #print(self.state)

        res = rmse.temperature_error() + rmse.humidity_error()
        if res <= self.goal:
            super(LayoutOptimization, self).set_user_exit(0,0)
        return res


if __name__ == '__main__':
    # state = random.sample(range(34), 2)
    # lay_opt = LayoutOptimization(state, 34, "../data/filter_data","../data/pos/pos.csv", 10)
    # lay_opt.copy_strategy = "slice"
    # lay_opt.steps = 10
    # lay_opt.updates = 10
    # state, e = lay_opt.anneal()
    # state = sorted(state)
    # print("root_mean_square_error: %f" % e)
    # print("final state: ", state)
    # print("-----end-----")
    # sensors = [lay_opt.sensor_num[item] for item in state]
    # sensors.append(str(e))
    # print("sensors:", sensors)

    # #对传感器的布局进行绘制
    # drawer = drawLayout('../data/pos/pos.csv','../draw/sensor.png',sensors)
    # drawer.main()

    # res = []
    # for i in range(3):
    #     state = random.sample(range(34), 15+i*5)
    #     lay_opt = LayoutOptimization(state, 34, "../data/filter_data","../data/pos/pos.csv", 10)
    #     lay_opt.copy_strategy = "slice"
    #     lay_opt.steps = 10000
    #     lay_opt.updates = 100
    #     state, e = lay_opt.anneal()
    #     state = sorted(state)
    #     print("root_mean_square_error: %f" % e)
    #     print("final state: ", state)
    #     print("-----end-----")
    #     sensors = [lay_opt.sensor_num[item] for item in state]
    #     sensors.append(str(e))
    #     print("sensors:", sensors)
    #     res.append(sensors)

    # csvfile = file('../data/result/layout_res.csv','wb')
    # writer = csv.writer(csvfile)
    # writer.writerows(res)
    # csvfile.close()

    res = []

    state = random.sample(range(34), 4)
    lay_opt = LayoutOptimization(state, 34, "../data/filter_data","../data/pos/pos.csv", 10, 2.46)
    # lay_opt.copy_strategy = "slice"
    # lay_opt.steps = 1000
    # lay_opt.updates = 1000
    # state, e = lay_opt.anneal()
    # state = sorted(state)
    # print("root_mean_square_error: %f" % e)
    # print("final state: ", state)
    # print("-----end-----")
    # sensors = [lay_opt.sensor_num[item] for item in state]
    # sensors.append(str(e))
    # print("sensors:", sensors)
    # res.append(sensors)

    # csvfile = file('../data/result/layout_res.csv','wb')
    # writer = csv.writer(csvfile)
    # writer.writerows(res)
    # csvfile.close()


    lay_opt.set_sensor_weight()

    cout = 0
    total = 1000
    for i in range(total):
        res = lay_opt.weight_select(['10728412','10728515'])
        if res == '10728412':
            cout+=1

    print cout
    print total-cout