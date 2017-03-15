#-*- coding:utf-8 -*-
import math
import random
import copy
import sys
import csv
sys.path.append("..")
from accuracy.root_mean_square_error import RMSE
from interpolation.ordinary_kriging import OrdinaryKriging

class LayoutValidation:
    def __init__(self, layout, number, filtered_file_path, pos_file_path, dis_file_path):
        #点的编号按照洞窟内传感器的布局，从低到高，从里到外，以便后续选点也按照这个顺序，这样可以在后续的图形绘制中体现出温湿度与布局的关系
        self.sensor_num = ['10728412','10728515','10728382','10728506','10728402','10728400','10728435','10728517','10728383',
        '10728534','10728432','10728401','10728391','10728437','10728525','10728399','10728518','10728442','10728527','10728390',
        '10728405','10728419','10728425','10728439','10728404','10728408','10728522','10728396','10728422','10728507','10728513',
        '10728387','10728385','10728519']
        self.layout = layout
        self.number = number
        self.filtered_file_path = filtered_file_path
        self.pos_file_path = pos_file_path
        self.dis_file_path = dis_file_path

    def generate(self):
        #将八个传感器的最优布局中的传感器点，任取一个和其余26个点中的一个进行互换，这样会生成8*26个布局，进行比较
        res = []
        tmp = []
        selected_list = self.layout
        unselected_list = [item for item in self.sensor_num if item not in selected_list]
        tmp.append(selected_list)
        tmp.append(unselected_list)
        res.append(tmp)

        for i in selected_list:
            for j in unselected_list:
                tmp = []
                t_selected_list = copy.deepcopy(selected_list)
                t_unselectec_list = copy.deepcopy(unselected_list)
                t_selected_list.remove(i)
                t_selected_list.append(j)
                t_unselectec_list.remove(j)
                t_unselectec_list.append(i)
                tmp.append(t_selected_list)
                tmp.append(t_unselectec_list)

                res.append(tmp)
        return res


    def random_generate(self):
        #随机生成8个传感器的布局
        res = []
        tmp = []
        selected_list = self.layout
        unselected_list = [item for item in self.sensor_num if item not in selected_list]
        tmp.append(selected_list)
        tmp.append(unselected_list)
        res.append(tmp)

        i = 0
        while i<self.number:
            selected_list = random.sample(self.sensor_num, len(self.layout))
            if set(selected_list) != set(self.layout):
                i+=1
                tmp = []
                unselected_list = [item for item in self.sensor_num if item not in selected_list]
                tmp.append(selected_list)
                tmp.append(unselected_list)

                res.append(tmp)
        return res

    def accuracy_calculate(self, ok3d_linear_res):
        error_ok3d_linear = RMSE(ok3d_linear_res)
        return error_ok3d_linear.temperature_error()+error_ok3d_linear.humidity_error()

    def validation(self, layout_validation_result_file_path, record_num, start_pos=0):
        res = self.generate()
        final_error = []
        for item in res:
            row = []
            selected_sensors,unselected_sensors = item[0],item[1]

            ok3d_linear = OrdinaryKriging(self.filtered_file_path,self.pos_file_path,selected_sensors,unselected_sensors, record_num, start_pos,'linear')
            ok3d_linear_res = ok3d_linear.run()

            final_error.append(self.accuracy_calculate(ok3d_linear_res))

        csvfile = file(layout_validation_result_file_path, 'wb')
        writer = csv.writer(csvfile)

        tmp_rows = [item[0] for item in res]
        writer.writerows(tmp_rows)
        writer.writerow(final_error)
        csvfile.close()

if __name__ == "__main__":
    layout = ['10728515','10728435','10728383','10728399','10728527','10728507','10728387','10728385']
    cv = LayoutValidation(layout, 15, "../data/filter_data","../data/pos/pos.csv","../data/pos/distance.csv")
    cv.validation("../data/result/layout_validation_result.csv",10, 100)
    print "done"