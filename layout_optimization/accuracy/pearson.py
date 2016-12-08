#-*- coding:utf-8 -*-
import sys
sys.path.append("..")
import math
from interpolation.ordinary_kriging import OrdinaryKriging
from interpolation.inverse_distance_weighted import InverseDistanceWeighted
from pick_tactics.tactics import PickTactics

class Pearson:
    """均方根误差"""
    def __init__(self, data):
        self.data = data

    def temperature_error(self):
        total = 0.0
        for group in self.data:
            average_prediction = 0.0
            average_real = 0.0
            for item in group:
                average_real += float(item[4])
                average_prediction += float(item[5])
            
            average_real /= len(group)
            average_prediction /= len(group)

            sum1 = 0.0
            sum2 = 0.0
            for item in group:
                sum1 += (float(item[4])-average_real)*(float(item[5])-average_prediction)
                sum2 += (float(item[4])-average_real)*(float(item[4])-average_real)*\
                    (float(item[5])-average_prediction)*(float(item[5])-average_prediction)

            total += sum1/math.sqrt(sum2)

        return total/len(self.data)

    def humidity_error(self):
        total = 0.0
        for group in self.data:
            average_prediction = 0.0
            average_real = 0.0
            for item in group:
                average_real += float(item[6])
                average_prediction += float(item[7])
            
            average_real /= len(group)
            average_prediction /= len(group)

            sum1 = 0.0
            sum2 = 0.0
            for item in group:
                sum1 += (float(item[6])-average_real)*(float(item[7])-average_prediction)
                sum2 += (float(item[6])-average_real)*(float(item[6])-average_real)*\
                    (float(item[7])-average_prediction)*(float(item[7])-average_prediction)

            total += sum1/math.sqrt(sum2)

        return total/len(self.data)

if __name__ == '__main__':
    tac = PickTactics()
    selected_sensors,unselected_sensors = tac.fixed_tactic([1, 2, 3, 4, 5, 11])
    ok3d = OrdinaryKriging("../data/filter_data","../data/pos/pos.csv",selected_sensors,unselected_sensors, 2)
    pearson1 = Pearson(ok3d.run())
    idw = InverseDistanceWeighted("../data/filter_data","../data/pos/pos.csv","../data/pos/distance.csv",selected_sensors,unselected_sensors,2)
    pearson2 = Pearson(idw.run())

    print pearson1.temperature_error()
    print pearson1.humidity_error()
    print pearson2.temperature_error()
    print pearson2.humidity_error()