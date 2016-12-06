#-*- coding:utf-8 -*-

import os
import sys
sys.path.append("..")
import csv
import math
from file_input_output.read_data import ReadData

__doc__ = '''用于计算各个传感器之间的距离'''

class DistanceCalculator:

    def __init__(self, pos_file_path, dis_file_path):
        self.pos_file_path = pos_file_path
        self.dis_file_path = dis_file_path

    def calculate(self):
        read_data = ReadData("", self.pos_file_path)
        pos_data = read_data.get_pos_data()

        sensors = pos_data.keys()
        distance_data = []
        for item1 in sensors:
            for item2 in sensors:
                pos1 = pos_data[item1]
                pos2 = pos_data[item2]
                square_dis = (float(pos1[0])/100-float(pos2[0])/100)*(float(pos1[0])/100-float(pos2[0])/100)+\
                            (float(pos1[1])/100-float(pos2[1])/100)*(float(pos1[1])/100-float(pos2[1])/100)+\
                            (float(pos1[2])/100-float(pos2[2])/100)*(float(pos1[2])/100-float(pos2[2])/100)
                #distance = math.sqrt(square_dis)
                #distance_data.append((item1, item2, distance))
                distance_data.append((item1, item2, square_dis))

        csvfile = file(self.dis_file_path, 'wb')
        writer = csv.writer(csvfile)
        writer.writerows(distance_data)
        csvfile.close()

if __name__ == '__main__':
    dis_cal = DistanceCalculator("../data/pos/pos.csv","../data/pos/distance.csv")
    dis_cal.calculate()