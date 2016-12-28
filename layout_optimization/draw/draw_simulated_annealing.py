#-*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import platform
import csv
import sys
import numpy as np
sys.path.append("..")

class DrawDifferentLayout:

    def draw(self):
        title = u'优化后的模拟退火算法迭代次数'

        majors = [u'三个',u'四个',u'五个',u'六个',u'七个',u'八个',u'九个',u'十个',u'十一个',u'十二个']


        file_data = [621,523,959,1457,967,2294,2578,2960,2791,2950]
        #print file_data
        color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c']

        sys_str = platform.system()
        if sys_str == 'Darwin':
            zhfont = mpl.font_manager.FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
        elif sys_str == 'Windows':
            zhfont = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')        
        

        plt.style.use('ggplot')
        fig, ax = plt.subplots(1, 1)

        ind = np.arange(len(file_data))
        width = 0.3
        rect = ax.bar(ind, file_data, width=0.6 ,color = color_sequence[0])

        plt.xlabel(u'传感器个数', fontproperties = zhfont, fontsize = 15)
        plt.ylabel(u'迭代次数', fontproperties = zhfont, fontsize = 15)
        #ax.set_xticks(range(len(majors)))
        ax.set_xticklabels(majors, fontproperties = zhfont, fontsize = 15)


        plt.title(title, fontproperties = zhfont, fontsize = 15)

        plt.show()
        #plt.savefig(u'../data/result/优化模拟退火算法对比图.png')

if __name__ == '__main__':
    draw_different_layout = DrawDifferentLayout()
    draw_different_layout.draw()