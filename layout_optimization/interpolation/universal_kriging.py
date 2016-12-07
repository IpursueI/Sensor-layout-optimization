#-*- coding:utf-8 -*-

import sys
sys.path.append("..")
import numpy
import csv
from pick_tactics.tactics import PickTactics
from pykrige.uk3d import UniversalKriging3D
from file_input_output.read_data import ReadData

__doc__ = '''用于泛kriging的计算'''

class UniversalKriging:

    def __init__(self, filtered_file_path, pos_file_path, selected_sensors, unselected_sensors, each_sensor_number, variogram_model='spherical'):
        self.filtered_file_path = filtered_file_path
        self.pos_file_path = pos_file_path
        self.selected_sensors = selected_sensors
        self.unselected_sensors = unselected_sensors
        self.each_sensor_number = each_sensor_number
        self.variogram_model = variogram_model

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
        read_data = ReadData(self.filtered_file_path, self.pos_file_path)
        self.temperature_humidity_data = read_data.get_temperature_humidity_data(self.each_sensor_number)
        self.pos_data = read_data.get_pos_data()

        calculate_data = []
        for item in self.selected_sensors:
            row_data = []
            for sensor_info in self.temperature_humidity_data[item]:
                row_data.append(list(self.pos_data[item]) + list(sensor_info))
            calculate_data.append(row_data)

        calculate_pos = []
        for item in self.unselected_sensors:
            calculate_pos.append(list(self.pos_data[item]))

        return calculate_data,calculate_pos


    def do_interpolate(self, data, grid_x, grid_y, grid_z, row_idx):
        #对温度进行插值
        uk3d_temp = UniversalKriging3D(data[:, 0], data[:, 1], data[:, 2], data[:, 3],variogram_model=self.variogram_model)
        #print data[:,1]
        #print gridx
        k3d_temp, ss3d_temp = uk3d_temp.execute('points', grid_x, grid_y, grid_z)
        
        #对湿度进行差值
        uk3d_hum = UniversalKriging3D(data[:, 0], data[:, 1], data[:, 2], data[:, 4],variogram_model=self.variogram_model)
        k3d_hum, ss3d_hum = uk3d_hum.execute('points', grid_x, grid_y, grid_z)
        
        #最后保存的数据，包括传感器编号，对应的x，y，z坐标，原始值，差值测量值
        final_data = []
        temp_var = 0
        hum_var = 0
        for idx in range(len(self.unselected_sensors)):
            row_data = []
            row_data.append(self.unselected_sensors[idx])
            row_data.append(self.pos_data[self.unselected_sensors[idx]][0])
            row_data.append(self.pos_data[self.unselected_sensors[idx]][1])
            row_data.append(self.pos_data[self.unselected_sensors[idx]][2])
            row_data.append(self.temperature_humidity_data[self.unselected_sensors[idx]][row_idx][0])  #温度
            row_data.append(str(k3d_temp[idx]))
            row_data.append(self.temperature_humidity_data[self.unselected_sensors[idx]][row_idx][1])  #湿度
            row_data.append(str(k3d_hum[idx]))
            
            original_temp = float(self.temperature_humidity_data[self.unselected_sensors[idx]][row_idx][0])
            original_hum = float(self.temperature_humidity_data[self.unselected_sensors[idx]][row_idx][1])
            temp_var += (original_temp-k3d_temp[idx])*(original_temp-k3d_temp[idx])
            hum_var += (original_hum-k3d_hum[idx])*(original_hum-k3d_hum[idx])
            final_data.append(row_data)
        
        return final_data
        #return temp_var/len(self.unselected_sensors),hum_var/len(self.unselected_sensors)


    def calculate(self):
        """
        each_row 格式：
        [[[x1,y1,z1,'14.649','20.323'], [[x2,y2,z2,'14.385','20.408']]]
        """

        calculate_data,calculate_pos = self.get_calculate_data()

        grid_x = []
        grid_y = []
        grid_z = []

        for item in calculate_pos:
            grid_x.append(item[0])
            grid_y.append(item[1])
            grid_z.append(item[2])

        grid_x = numpy.array([float(i) for i in grid_x])
        grid_y = numpy.array([float(i) for i in grid_y])
        grid_z = numpy.array([float(i) for i in grid_z])

        min_calculate_data_len = min([len(item) for item in calculate_data])

        final_result = []
        for index in range(min_calculate_data_len):
            each_row = []
            for col_item in calculate_data:
                each_row.append([float(item) for item in col_item[index]])

            final_data = numpy.array(each_row)

            final_result.append(self.do_interpolate(final_data, grid_x, grid_y, grid_z, index))

        return final_result

    def run(self):
        #calculate_data,calculate_pos = self.get_calculate_data()
        #return self.calculate(calculate_data, calculate_pos)
        return self.calculate()

if __name__ == '__main__':
    pick = PickTactics()
    #selected_sensors,unselected_sensors = pick.random_tactic(10)
    selected_sensors,unselected_sensors = pick.fixed_tactic([1,5,10,15,25])
    uk3d = UniversalKriging("../data/filter_data","../data/pos/pos.csv",selected_sensors,unselected_sensors,2)
    print uk3d.run()