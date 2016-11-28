#-*- coding:utf-8 -*-

import os
import sys
import csv

class FilterData:
    """从原始的洞窟温湿度数据中挑选部分数据。

    一共34个传感器，每个传感器的数据存放在一个csv文件中
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def get_file_names(self):
        file_list = os.listdir(self.file_path)
        self.file_list = [item for item in file_list if item.endswith('.csv')]
        #print self.file_list
        #print len(self.file_list)


    def filter(self, file_input, file_output, start_row = 2, step = 10):
        csv_file = file(file_input, 'rb')
        reader = csv.reader(csv_file)
        tmp_data = [line for line in reader]

        #每个文件的末尾含有一些无用数据，因此删除一些
        file_len = len(tmp_data)-4
        		
        #根据起始行和步长提取出文件中的数据，文件格式为  [传感器编号，温度，湿度]
        file_data = [(tmp_data[i][2], tmp_data[i][3]) for i in range(start_row, file_len, step)]

        csv_file_res = file(file_output, 'w')
        csv_writer = csv.writer(csv_file_res)
        csv_writer.writerows(file_data)
        csv_file_res.close()

    def write_filter_data(self):

        for item in self.file_list:

            file_input = os.path.join(self.file_path, item)
            file_output = os.path.join(os.path.join(self.file_path, "filter_data"), "filtered_"+item)
            self.filter(file_input, file_output)


if __name__ == '__main__':
    filter_data = FilterData("../data")
    filter_data.get_file_names()
    filter_data.write_filter_data()