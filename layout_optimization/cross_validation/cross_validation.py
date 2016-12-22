#-*- coding:utf-8 -*-
import math
import sys
import csv
sys.path.append("..")
from accuracy.root_mean_square_error import RMSE
from accuracy.pearson import Pearson
from accuracy.mean_error import MeanError
from interpolation.ordinary_kriging import OrdinaryKriging
from interpolation.universal_kriging import UniversalKriging
from interpolation.inverse_distance_weighted import InverseDistanceWeighted

class CrossValidation:
    def __init__(self, class_count, sensor_count, filtered_file_path, pos_file_path, dis_file_path):
        #点的编号按照洞窟内传感器的布局，从低到高，从里到外，以便后续选点也按照这个顺序，这样可以在后续的图形绘制中体现出温湿度与布局的关系
        self.sensor_num = ['10728412','10728515','10728382','10728506','10728402','10728400','10728435','10728517','10728383',
        '10728534','10728432','10728401','10728391','10728437','10728525','10728399','10728518','10728442','10728527','10728390',
        '10728405','10728419','10728425','10728439','10728404','10728408','10728522','10728396','10728422','10728507','10728513',
        '10728387','10728385','10728519']
        self.class_count = class_count
        self.sensor_count = sensor_count
        self.filtered_file_path = filtered_file_path
        self.pos_file_path = pos_file_path
        self.dis_file_path = dis_file_path

    def generate(self):
        num = range(self.sensor_count)
        member_count = int(math.ceil(float(self.sensor_count)/self.class_count))
        start = 0
        class_list = []
        for i in range(self.class_count):
            tmp = []
            for j in range(member_count):
                if start < self.sensor_count:
                    tmp.append(start)
                    start += 1
            class_list.append(tmp)

        #print 'class list:'
        #print class_list

        result = []
        set_all = set(range(self.sensor_count))
        for i in range(self.class_count):
            item = []
            selected_list = list(set_all.difference(set(class_list[i])))
            #print selected_list
            #print class_list[i]
            selected_list = [self.sensor_num[j] for j in selected_list]
            unselected_list = [self.sensor_num[j] for j in class_list[i]]
            item.append(selected_list)
            item.append(unselected_list)
            result.append(item)

        return result


    def accuracy_calculate(self, error_type, idw_res, ok3d_spherical_res, ok3d_linear_res, ok3d_power_res, ok3d_exponential_res):
        if error_type == 0:
            error_idw = RMSE(idw_res)
            error_ok3d_spherical = RMSE(ok3d_spherical_res)
            error_ok3d_linear = RMSE(ok3d_linear_res)
            error_ok3d_power = RMSE(ok3d_power_res)
            #error_ok3d_gaussian = RMSE(ok3d_gaussian_res)
            error_ok3d_exponential = RMSE(ok3d_exponential_res)
        elif error_type == 1:
            error_idw = MeanError(idw_res)
            error_ok3d_spherical = MeanError(ok3d_spherical_res)
            error_ok3d_linear = MeanError(ok3d_linear_res)
            error_ok3d_power = MeanError(ok3d_power_res)
            #error_ok3d_gaussian = MeanError(ok3d_gaussian_res)
            error_ok3d_exponential = MeanError(ok3d_exponential_res)
        elif error_type == 2:
            error_idw = Pearson(idw_res)
            error_ok3d_spherical = Pearson(ok3d_spherical_res)
            error_ok3d_linear = Pearson(ok3d_linear_res)
            error_ok3d_power = Pearson(ok3d_power_res)
            #error_ok3d_gaussian = Pearson(ok3d_gaussian_res)
            error_ok3d_exponential = Pearson(ok3d_exponential_res)

        return [error_idw.temperature_error(), error_idw.humidity_error(),
                error_ok3d_spherical.temperature_error(), error_ok3d_spherical.humidity_error(),
                error_ok3d_linear.temperature_error(), error_ok3d_linear.humidity_error(),
                error_ok3d_power.temperature_error(), error_ok3d_power.humidity_error(),
                #error_ok3d_gaussian.temperature_error(), error_ok3d_gaussian.humidity_error(),
                error_ok3d_exponential.temperature_error(), error_ok3d_exponential.humidity_error()]

    def validation(self, validation_result_file_path, record_num):
        res = self.generate()
        final_error = []
        average_error = [[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                        [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                        [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]]
        for item in res:
            row = []
            selected_sensors,unselected_sensors = item[0],item[1]
            idw = InverseDistanceWeighted(self.filtered_file_path,self.pos_file_path,self.dis_file_path,selected_sensors,unselected_sensors,record_num)
            idw_res = idw.run()
            
            ok3d_spherical = OrdinaryKriging(self.filtered_file_path,self.pos_file_path,selected_sensors,unselected_sensors, record_num, 'spherical')
            ok3d_spherical_res = ok3d_spherical.run()

            ok3d_linear = OrdinaryKriging(self.filtered_file_path,self.pos_file_path,selected_sensors,unselected_sensors, record_num, 'linear')
            ok3d_linear_res = ok3d_linear.run()

            ok3d_power = OrdinaryKriging(self.filtered_file_path,self.pos_file_path,selected_sensors,unselected_sensors, record_num, 'power')
            ok3d_power_res = ok3d_power.run()

            #ok3d_gaussian = OrdinaryKriging(self.filtered_file_path,self.pos_file_path,selected_sensors,unselected_sensors, record_num, 'gaussian')
            #ok3d_gaussian_res = ok3d_gaussian.run()

            ok3d_exponential = OrdinaryKriging(self.filtered_file_path,self.pos_file_path,selected_sensors,unselected_sensors, record_num, 'exponential')
            ok3d_exponential_res = ok3d_exponential.run()

            for i in range(3):
                cal_res = self.accuracy_calculate(i, idw_res, ok3d_spherical_res, ok3d_linear_res, ok3d_power_res, ok3d_exponential_res)
                row.append(cal_res)

            for j in range(len(average_error)):
                for k in range(len(average_error[0])):
                    average_error[j][k] += row[j][k]

            final_error.append(row) 

        #print average_error
        average_error = [[j/len(res) for j in i] for i in average_error]
        #print average_error
        
        for i in range(3):
            csvfile = file(validation_result_file_path[i], 'wb')
            writer = csv.writer(csvfile)
            writer.writerow(['idw温度','idw湿度','kriging_spherical温度','kriging_spherical湿度',
                                'kriging_linear温度','kriging_linear湿度','kriging_power温度','kriging_power湿度',
                                #'kriging_gaussian温度','kriging_gaussian湿度',
                                'kriging_exponential温度','kriging_exponential湿度'])
            tmp_rows = [item[i] for item in final_error]
            writer.writerows(tmp_rows)
            writer.writerow(['平均值','平均值','平均值','平均值','平均值','平均值','平均值','平均值','平均值','平均值'])
            writer.writerow(average_error[i])
            csvfile.close()

if __name__ == "__main__":
    cv = CrossValidation(7, 34, "../data/filter_data","../data/pos/pos.csv","../data/pos/distance.csv")
    cv.validation(["../data/result/RMSE.csv", "../data/result/MeanError.csv", "../data/result/Pearson.csv"],10)
    print "done"