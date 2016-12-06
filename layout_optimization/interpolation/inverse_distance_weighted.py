#-*- coding:utf-8 -*-

import sys
sys.path.append("..")
import numpy
import csv
from pick_tactics.tactics import PickTactics
from file_input_output.read_data import ReadData

__doc__ = '''用于反距离加权法计算'''

class InverseDistanceWeighted:
    def __init__(self, filtered_file_path, pos_file_path, dis_file_path, selected_sensors, unselected_sensors, each_sensor_number):
        self.filtered_file_path = filtered_file_path
        self.pos_file_path = pos_file_path
        self.dis_file_path = dis_file_path
        self.selected_sensors = selected_sensors
        self.unselected_sensors = unselected_sensors
        self.each_sensor_number = each_sensor_number

    def get_calculate_data(self):
        """
        temperature_humidity_data 格式：
        {'10728442': [['14.649', '20.323'], ['14.529', '20.012']], '10728383': [['14.385', '20.408'], ['14.337', '20.101']]}

        calculate_data 格式：
        [[[x1,y1,z1,'14.649','20.323'],[x1,y1,z1,'14.529','20.012']], [[x2,y2,z2,'14.385','20.408'],[x2,y2,z2,'14.337','20.101']]]

        pos_data 格式：
        {'10728442': ('920', '0', '360'), '10728404': ('1450', '460', '0')}

        calculate_pos 格式：
        [[x1,y1,z1],[x2,y2,z2]]
        """
        read_data = ReadData(self.filtered_file_path, self.pos_file_path, self.dis_file_path)
        self.temperature_humidity_data = read_data.get_temperature_humidity_data(self.each_sensor_number)
        self.pos_data = read_data.get_pos_data()
        self.dis_data = read_data.get_dis_data()
        #print self.dis_data
        calculate_data = []
        for item in self.selected_sensors:
            row_data = []
            for sensor_info in self.temperature_humidity_data[item]:
                row_data.append([item]+list(self.pos_data[item]) + list(sensor_info))
            calculate_data.append(row_data)

        calculate_pos = []
        for item in self.unselected_sensors:
            calculate_pos.append(list(self.pos_data[item]))

        return calculate_data,calculate_pos

    def do_interpolate(self, sensors, row_idx):
        final_data = []
        #print self.dis_data
        for item in self.unselected_sensors:
            row_data = []
            temp_sum = 0.0
            hum_sum = 0.0
            coefficient_sum = 0.0
            for sensor in sensors:
                tmp = 1/float(self.dis_data[sensor[0]][item])
                temp_sum += tmp*sensor[4]
                hum_sum += tmp*sensor[5]
                coefficient_sum += tmp

            temp = temp_sum/coefficient_sum
            hum = hum_sum/coefficient_sum

            row_data.append(item)
            row_data.append(self.pos_data[item][0])
            row_data.append(self.pos_data[item][1])
            row_data.append(self.pos_data[item][2])
            row_data.append(self.temperature_humidity_data[item][row_idx][0])
            row_data.append(temp)
            row_data.append(self.temperature_humidity_data[item][row_idx][1])
            row_data.append(hum)

            final_data.append(row_data)

        return final_data

    def calculate(self):
        calculate_data,calculate_pos = self.get_calculate_data()
        min_calculate_data_len = min([len(item) for item in calculate_data])
        final_result = []
        for index in range(min_calculate_data_len):
            each_row = []
            for col_item in calculate_data:
                each_row.append([col_item[index][0]] + [float(item) for item in col_item[index][1:]])

            final_result.append(self.do_interpolate(each_row, index))
        return final_result

    def run(self):
        return self.calculate()

if __name__ == '__main__':
    pick = PickTactics()
    selected_sensors,unselected_sensors = pick.random_tactic(10)
    idw = InverseDistanceWeighted("../data/filter_data","../data/pos/pos.csv","../data/pos/distance.csv",selected_sensors,unselected_sensors,2)
    print idw.run()