#!/usr/bin/python
#-*- coding:utf-8 -*-

__doc__ = '''
本文件主要涉及传感器的选择策略
'''

import random

class PickTactics:
    def __init__(self):
        #点的编号按照洞窟内传感器的布局，从低到高，从里到外，以便后续选点也按照这个顺序，这样可以在后续的图形绘制中体现出温湿度与布局的关系
        self.sensor_num = ['10728412','10728515','10728382','10728506','10728402','10728400','10728435','10728517','10728383',
        '10728534','10728432','10728401','10728391','10728437','10728525','10728399','10728518','10728442','10728527','10728390',
        '10728405','10728419','10728425','10728439','10728404','10728408','10728522','10728396','10728422','10728507','10728513',
        '10728387','10728385','10728519']

        self.total = 34
        
    def get_all_sensor(self):
        return self.sensor_num
        
    #根据传入的传感器个数，随机挑选传感器
    def random_tactic(self, number):
        list_slice =  random.sample(range(0, self.total), number)
        
        #对随机出来的点进行排序
        list_slice.sort()
        selected_list = [self.sensor_num[i] for i in list_slice]
        unselected_list = [item for item in self.sensor_num if item not in selected_list]
        return selected_list, unselected_list

    #给出固定的传感器序列，列表取值范围时0-33
    def fixed_tactic(self, listc):
        selected_list = [self.sensor_num[i] for i in listc]
        unselected_list = [item for item in self.sensor_num if item not in selected_list]
        return selected_list, unselected_list
        
if __name__ == '__main__':
    tac = PickTactics()
    print tac.random_tactic(10)
    print tac.fixed_tactic([0,1,2])
    
