#-*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import platform
import csv

class DrawAveragePearson:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path

    def get_data(self, temp_hum):  #temp_hum=0时代表温度，1代表湿度
        file_data = []
        with open(self.data_file_path) as f:
            f_csv = csv.reader(f)
            for index,row in enumerate(f_csv):
                if index == 9:
                    file_data = [float(item) for item in row]
        if temp_hum == 0:
            file_data = file_data[::2]
        elif temp_hum == 1:
            file_data = file_data[1::2]

        return file_data


    def draw(self, temp_hum):
        #title = ['Temperature interpolation average pearson cross_validation','humidity interpolation average pearson cross_validation']
        title = [u'温度pearson相关系数均值',u'湿度pearson相关系数均值']

        majors = [['idw_temp','kriging_spherical_temp','kriging_linear_temp',
                    'kriging_power_temp','kriging_exponential_temp'],
                    ['idw_hum','kriging_spherical_hum','kriging_linear_hum',
                    'kriging_power_hum','kriging_exponential_hum']]

        y_offsets = {'idw_temp':0.5, 'kriging_spherical_temp':0.5, 'kriging_linear_temp':0.4,
                        'kriging_power_temp':0.5, 'kriging_gaussian_temp':0.5, 'kriging_exponential_temp':0.5,
                        'idw_hum':0.5, 'kriging_spherical_hum':0.4, 'kriging_linear_hum':0.5,
                        'kriging_power_hum':0.5, 'kriging_gaussian_hum':0.5, 'kriging_exponential_hum':0.5}

        file_data = self.get_data(temp_hum)
        print file_data
        color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c']
        plt.style.use('ggplot')
        fig, ax = plt.subplots(1, 1, figsize=(12, 14))

        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()


        sys_str = platform.system()
        if sys_str == 'Darwin':
            zhfont = mpl.font_manager.FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
        elif sys_str == 'Windows':
            zhfont = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')        
        plt.xlabel(u'插值方法或者模型类型', fontproperties = zhfont, fontsize = 15)
        plt.ylabel(u'pearson相关系数均值', fontproperties = zhfont, fontsize = 15)

        ax.set_xticks(range(5))
        ax.set_xticklabels(majors[temp_hum])

        plt.xlim(-0.5,4.5)
        if temp_hum == 0:
            plt.ylim(1.0, 1.5)
        elif temp_hum == 1:
            plt.ylim(-0.4,1.2)


        line = plt.plot(range(5), file_data,lw=2.5,color=color_sequence[0])

        y_pos = file_data[-1] - 0.5

        #plt.text(5.2, y_pos, "average RMSE", fontsize=14, color=color_sequence[0])

        #plt.title(title[temp_hum], fontsize=18, ha='center')
        plt.title(title[temp_hum], fontproperties = zhfont, fontsize = 15)

        #plt.show()
        if temp_hum == 0:
            plt.savefig(u'../data/result/温度pearson相关系数均值图.png')
        else:
            plt.savefig(u'../data/result/湿度pearson相关系数均值图.png')


if __name__ == '__main__':
    draw_average_pearson = DrawAveragePearson("../data/result/Pearson.csv")
    draw_average_pearson.draw(1)
    #draw_average_pearson.draw(1)