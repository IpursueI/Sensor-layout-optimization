#-*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import platform
import numpy as np
import csv
import sys
sys.path.append("..")
from draw.draw_layout import drawLayout

class DrawLayoutValidation2:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path

    def get_data(self):  #temp_hum=0时代表温度，1代表湿度
        file_data = []
        with open(self.data_file_path) as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                file_data.append(row)
        return file_data


    def draw(self):

        file_data = self.get_data()
        color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c']
        plt.style.use('ggplot')
        fig, ax = plt.subplots(1, 1)

        sys_str = platform.system()
        if sys_str == 'Darwin':
            zhfont = mpl.font_manager.FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
        elif sys_str == 'Windows':
            zhfont = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')

        data = [float(item) for item in file_data[-1]]
        weights = np.ones_like(data)/float(len(data))
        n, bins, patches = plt.hist(data,20,weights=weights)

        X, Y =  np.zeros(10),np.linspace(0, 100, 10)
        #ax.plot(X+1.947276, Y, linestyle=(0, (3, 5, 1, 5, 1, 5)), linewidth=1.5, color='black')
        print n
        print bins

        plt.xlabel(u'均方根误差', fontproperties = zhfont, fontsize = 15)
        plt.ylabel(u'概率', fontproperties = zhfont, fontsize = 15)

        plt.title(u'传感器插值误差概率分布图', fontproperties = zhfont, fontsize = 15)

        plt.show()
        #plt.savefig(u'../data/result/传感器插值误差直方图.png')


if __name__ == '__main__':
    draw_layout_validation = DrawLayoutValidation2("../data/result/layout_validation_result.csv")
    draw_layout_validation.draw()