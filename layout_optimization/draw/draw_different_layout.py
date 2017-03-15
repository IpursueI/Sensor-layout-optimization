#-*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import platform
import csv
import sys
sys.path.append("..")
from draw.draw_layout import drawLayout

class DrawDifferentLayout:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path

    def get_data(self):  #temp_hum=0时代表温度，1代表湿度
        file_data = []
        with open(self.data_file_path) as f:
            f_csv = csv.reader(f)
            start_count = 4
            for row in f_csv:
                file_data.append(row[:start_count])
                start_count += 1

        return file_data


    def draw(self):
        title = u'不同传感器个数最优布局均方根误差'

        majors = ['3','4','5','6','7','8','9','10','11','12']


        file_data = self.get_data()
        print file_data
        color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c']

        plt.style.use('ggplot')
        fig, ax = plt.subplots(1, 1)


        sys_str = platform.system()
        if sys_str == 'Darwin':
            zhfont = mpl.font_manager.FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
        elif sys_str == 'Windows':
            zhfont = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')        
        plt.xlabel(u'传感器个数', fontproperties = zhfont, fontsize = 15)
        plt.ylabel(u'均方根误差', fontproperties = zhfont, fontsize = 15)

        ax.set_xticks(range(len(majors)))
        ax.set_xticklabels(majors, fontproperties = zhfont, fontsize = 15)

        res_data = [item[-1] for item in file_data][:len(majors)]

        line = plt.plot(range(len(majors)), res_data,lw=2.5,color=color_sequence[0])

        plt.title(title, fontproperties = zhfont, fontsize = 15)

        #plt.show()
        plt.savefig(u'../data/result/不同传感器个数最优布局均方根误差图.png')

    def draw_layout(self,number):
        #对传感器的布局进行绘制
        file_data = self.get_data()
        sensors = file_data[number]
        drawer = drawLayout('../data/pos/pos.csv','../draw/sensor.png',sensors)
        drawer.main()

if __name__ == '__main__':
    draw_different_layout = DrawDifferentLayout("../data/result/layout_res_backup.csv")
    draw_different_layout.draw()
    #draw_different_layout.draw_layout(9)