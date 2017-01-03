#-*- coding:utf-8 -*-
import math
import sys
import csv
sys.path.append("..")
from accuracy.root_mean_square_error import RMSE
from interpolation.ordinary_kriging import OrdinaryKriging


class SensorWeight:
    def __init__(self, filtered_file_path, pos_file_path, dis_file_path):
 
        self.filtered_file_path = filtered_file_path
        self.pos_file_path = pos_file_path
        self.dis_file_path = dis_file_path

    def generate(self):

        sensor_group = [['10728382','10728515','10728412'],['10728400','10728402','10728506'],['10728383','10728517','10728435'],
                        ['10728401','10728432','10728534'],['10728525','10728437','10728391'],['10728442','10728518','10728399',],
                        ['10728405','10728390','10728527'],['10728439','10728425','10728419'],['10728396','10728522','10728408','10728404'],
                        ['10728513','10728507','10728422'],['10728519','10728385','10728387']]

        result = []
        for i in range(len(sensor_group)):
            item = []
            selected_list = sensor_group[i]
            unselected_list = []
            for j in range(len(sensor_group)):
                if j != i:
                    unselected_list.extend(sensor_group[j])
            item.append(selected_list)
            item.append(unselected_list)
            result.append(item)
        return result


    def accuracy_calculate(self, ok3d_linear_res):
        error_ok3d_linear = RMSE(ok3d_linear_res)
        return error_ok3d_linear.temperature_error()+error_ok3d_linear.humidity_error()

    def validation(self, validation_result_file_path, record_num):
        res = self.generate()
        final_error = []

        for item in res:
            selected_sensors,unselected_sensors = item[0],item[1]
            #print selected_sensors
            #print unselected_sensors

            ok3d_linear = OrdinaryKriging(self.filtered_file_path,self.pos_file_path,selected_sensors,unselected_sensors, record_num, 0,'linear')
            ok3d_linear_res = ok3d_linear.run()
            #print ok3d_linear_res
            cal_res = self.accuracy_calculate(ok3d_linear_res)
            final_error.append(cal_res)


        #print final_error
        csvfile = file(validation_result_file_path, 'wb')
        writer = csv.writer(csvfile)
        writer.writerow(final_error)
        csvfile.close()

if __name__ == "__main__":
    cv = SensorWeight("../data/filter_data","../data/pos/pos.csv","../data/pos/distance.csv")
    cv.validation("../data/result/sensor_weight.csv",10)
    print "done"