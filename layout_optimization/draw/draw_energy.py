#-*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import platform
import csv
import numpy as np

class DrawEnergy:
    def get_data(self, data_file_path):
        file_data = []
        with open(data_file_path) as f:
            f_csv = csv.reader(f)
            data = [item for item in f_csv]
        return data


    def draw(self, data_file_path, start_line):

        result_file_path = u'../data/result/模拟退火迭代过程图.png'

        file_data = self.get_data(data_file_path)
        #print file_data
        color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c']
        plt.style.use('ggplot')
        fig, ax = plt.subplots(1, 1)

        sys_str = platform.system()
        if sys_str == 'Darwin':
            zhfont = mpl.font_manager.FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
        elif sys_str == 'Windows':
            zhfont = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')

        plt.xlabel(u'迭代次数', fontproperties = zhfont, fontsize = 15)
        plt.ylabel(u'均方根误差', fontproperties = zhfont, fontsize = 15)
        #ax.set_xticks(ind+width/2)
        #ax.set_xticklabels(range(1,len(file_data[0])+1))

        plt.title(u'模拟退火迭代过程图', fontproperties = zhfont, fontsize = 15)
        print file_data
        plt.plot(range(1, len(file_data[start_line])+1), file_data[start_line])
        plt.plot(range(1, len(file_data[start_line+2])+1), file_data[start_line+2])
        #plt.savefig(result_file_path)
        plt.show()
        


if __name__ == '__main__':
    dsw = DrawEnergy()
    dsw.draw("../data/result/energy_record.csv",0)