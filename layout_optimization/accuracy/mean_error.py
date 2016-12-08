#-*- coding:utf-8 -*-
import sys
sys.path.append("..")
import math
from interpolation.ordinary_kriging import OrdinaryKriging
from pick_tactics.tactics import PickTactics

class MeanError:
    """平均误差"""
    def __init__(self, data):
        self.data = data

    def temperature_error(self):
        total = 0.0
        for group in self.data:
            tmp = 0.0
            for item in group:
                tmp += (float(item[5])-float(item[4]))

            total += tmp/len(group)

        return total/len(self.data)

    def humidity_error(self):
        total = 0.0
        for group in self.data:
            tmp = 0.0
            for item in group:
                tmp += (float(item[7])-float(item[6]))

            total += tmp/len(group)

        return total/len(self.data)

if __name__ == '__main__':
    tac = PickTactics()
    selected_sensors,unselected_sensors = tac.fixed_tactic([31, 32, 12, 7, 3, 11])
    ok3d = OrdinaryKriging("../data/filter_data","../data/pos/pos.csv",selected_sensors,unselected_sensors, 2)
    me = MeanError(ok3d.run())
    print me.temperature_error()
    print me.humidity_error()