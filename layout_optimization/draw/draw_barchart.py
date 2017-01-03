#-*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import platform
import csv
import numpy as np

class DrawBarChart:
    def get_data(self, data_file_path, temp_hum, start,end):  #temp_hum=0时代表温度，1代表湿度
        file_data = []
        with open(data_file_path) as f:
            f_csv = csv.reader(f)
            data = [item for item in f_csv]
            for row in data[start:end]:
                row = [float(item) for item in row]
                file_data.append(row)

        column = range(10)[temp_hum::2]
        res = []
        for item in column:
            #print "item:",item
            row_data = []
            for row in file_data:
                row_data.append(row[item])
            res.append(row_data)

        return res


    def draw(self, start, end, data_file_path, temp_hum, error_type):
        titles = [[u'温度插值平均误差',u'温度插值均方根误差',u'温度插值pearson相关系数'], [u'湿度插值平均误差',u'湿度插值均方根误差', u'湿度插值pearson相关系数']]
        
        ylabels = [u'平均误差',u'均方根误差',u'Pearson相关系数']

        result_file_path = [[u'../data/result/温度插值平均误差条形图.png',u'../data/result/温度插值均方根误差条形图.png',u'../data/result/温度插值pearson相关系数条形图.png'], 
            [u'../data/result/湿度插值平均误差条形图.png',u'../data/result/湿度插值均方根误差条形图.png', u'../data/result/湿度插值pearson相关系数条形图.png']]

        majors = ['idw','kriging_spherical','kriging_linear',
                    'kriging_power','kriging_exponential']

        file_data = self.get_data(data_file_path, temp_hum, start,end)
        #print file_data
        color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c']
        plt.style.use('ggplot')
        fig, ax = plt.subplots(1, 1)

        ind = np.arange(end-start)
        width = 0.15
        rects = []
        for i in range(5):
            rect = ax.bar(ind+i*width, file_data[i], width, color = color_sequence[i])
            rects.append(rect)

        sys_str = platform.system()
        if sys_str == 'Darwin':
            zhfont = mpl.font_manager.FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
        elif sys_str == 'Windows':
            zhfont = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')

        plt.xlabel(u'传感器布局编号', fontproperties = zhfont, fontsize = 15)
        plt.ylabel(ylabels[error_type], fontproperties = zhfont, fontsize = 15)
        ax.set_xticks(ind+width*2.5)
        #ax.set_xticklabels((u'实验1', u'实验2', u'实验3', u'实验4', u'实验5',u'实验6', u'实验7'), fontproperties = zhfont, fontsize = 15)
        ax.set_xticklabels([start+item for item in range(end-start)])

        plt.title(titles[temp_hum][error_type], fontproperties = zhfont, fontsize = 15)

        ax.legend((rects[0], rects[1], rects[2], rects[3], rects[4]), majors, loc=0)

        
        plt.savefig(result_file_path[temp_hum][error_type])
        #plt.show()
        


if __name__ == '__main__':
    dbc = DrawBarChart()
    files = ["../data/result/MeanError.csv", "../data/result/RMSE.csv", "../data/result/Pearson.csv"]
    
    result_file_path = []

    # for i in range(2):
    #     #for j in range(3):
    #     dbc.draw(1,11,files[1], i, 1)

    #dbc.draw(1,11,files[1], 0, 1)    #前十组数据 温度 均方根误差
    #dbc.draw(11,21,files[1], 0, 1)   #后十组数据
    #dbc.draw(1,11,files[1], 1, 1)
    dbc.draw(11,21,files[1], 1, 1)