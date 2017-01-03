#-*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import platform
import csv
import numpy as np

class DrawMeanBarChart:
    def get_data(self, data_file_path, temp_hum):  #temp_hum=0时代表温度，1代表湿度
        file_data = []
        with open(data_file_path) as f:
            f_csv = csv.reader(f)
            data = [item for item in f_csv]
            file_data = [float(item) for item in data[-1]]
        if temp_hum == 0:
            file_data = file_data[::2]
        elif temp_hum == 1:
            file_data = file_data[1::2]

        return file_data


    def draw(self, data_file_path, temp_hum, error_type):
        titles = [[u'温度插值平均误差均值',u'温度插值均方根误差均值',u'温度插值pearson相关系数均值'], [u'湿度插值平均误差均值',u'湿度插值均方根误差均值', u'湿度插值pearson相关系数均值']]
        
        ylabels = [u'平均误差均值',u'均方根误差均值',u'Pearson相关系数均值']

        result_file_path = [[u'../data/result/温度插值平均误差均值条形图.png',u'../data/result/温度插值均方根误差均值条形图.png',u'../data/result/温度插值pearson相关系数均值条形图.png'], 
            [u'../data/result/湿度插值平均误差均值条形图.png',u'../data/result/湿度插值均方根误差均值条形图.png', u'../data/result/湿度插值pearson相关系数均值条形图.png']]

        majors = ['idw','kriging_spherical','kriging_linear',
                    'kriging_power','kriging_exponential']

        file_data = self.get_data(data_file_path, temp_hum)
        print file_data
        color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c']
        plt.style.use('ggplot')
        fig, ax = plt.subplots(1, 1)

        ind = np.arange(5)
        width = 0.6
        rect = ax.bar(ind, file_data, width ,color = color_sequence[0])

        sys_str = platform.system()
        if sys_str == 'Darwin':
            zhfont = mpl.font_manager.FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
        elif sys_str == 'Windows':
            zhfont = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')

        plt.xlabel(u'插值或者模型类型', fontproperties = zhfont, fontsize = 15)
        plt.ylabel(ylabels[error_type], fontproperties = zhfont, fontsize = 15)
        ax.set_xticks(ind+width/2)
        ax.set_xticklabels(majors)

        plt.title(titles[temp_hum][error_type], fontproperties = zhfont, fontsize = 15)

        
        #plt.savefig(result_file_path[temp_hum][error_type])
        plt.show()
        


if __name__ == '__main__':
    dbc = DrawMeanBarChart()
    files = ["../data/result/MeanError.csv", "../data/result/RMSE.csv", "../data/result/Pearson.csv"]

    for i in range(2):
        #for j in range(3):
        dbc.draw(files[1], i, 1)

    #dbc.draw(files[0], 0, 0)