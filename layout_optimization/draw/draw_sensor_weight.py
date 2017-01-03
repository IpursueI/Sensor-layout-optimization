#-*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import platform
import csv
import numpy as np

class DrawSensorWeight:
    def get_data(self, data_file_path):
        file_data = []
        with open(data_file_path) as f:
            f_csv = csv.reader(f)
            data = [item for item in f_csv]
            file_data = [float(item) for item in data[0]]

        return file_data


    def draw(self, data_file_path, group_number):
        title = u'温湿度插值均方根误差'
        ylabel = u'均方根误差'

        result_file_path = u'../data/result/传感器权重条形图.png'

        file_data = self.get_data(data_file_path)
        print file_data
        color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c']
        plt.style.use('ggplot')
        fig, ax = plt.subplots(1, 1)

        ind = np.arange(group_number)
        width = 0.6
        rect = ax.bar(ind, file_data, width ,color = color_sequence[0])

        sys_str = platform.system()
        if sys_str == 'Darwin':
            zhfont = mpl.font_manager.FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
        elif sys_str == 'Windows':
            zhfont = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')

        plt.xlabel(u'插值实验编号', fontproperties = zhfont, fontsize = 15)
        plt.ylabel(ylabel, fontproperties = zhfont, fontsize = 15)
        ax.set_xticks(ind+width/2)
        ax.set_xticklabels(range(1,group_number+1))

        plt.title(title, fontproperties = zhfont, fontsize = 15)

        
        plt.savefig(result_file_path)
        plt.show()
        


if __name__ == '__main__':
    dsw = DrawSensorWeight()
    dsw.draw("../data/result/sensor_weight.csv", 11)