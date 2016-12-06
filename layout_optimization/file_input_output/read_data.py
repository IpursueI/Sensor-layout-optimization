#-*- coding:utf-8 -*-

import os
import sys
import csv

class ReadData:
    def __init__(self, filtered_file_path, pos_file_path, dis_file_path=""):
        self.filtered_file_path = filtered_file_path
        self.pos_file_path = pos_file_path
        self.dis_file_path = dis_file_path

    def get_file_names(self):
        file_list = os.listdir(self.filtered_file_path)
        return [item for item in file_list if item.endswith('.csv')]

    def get_pos_data(self):
        pos_data = {}
        with open(self.pos_file_path) as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                pos_data[row[0]] = (row[1], row[2],row[3])
            return pos_data

    def get_dis_data(self):
        dis_data = {}
        with open(self.dis_file_path) as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                if dis_data.has_key(row[0]):
                    dis_data[row[0]][row[1]] = row[2]
                else:
                    value = {}
                    value[row[1]] = row[2]
                    dis_data[row[0]] = value
            return dis_data

    def get_temperature_humidity_data(self, number):
        temperature_humidity_data = {}
        file_list = self.get_file_names()
        for file_name in file_list:
            file_path = os.path.join(self.filtered_file_path, file_name)
            csv_file = file(file_path, 'rb')
            reader = csv.reader(csv_file)
            file_data = [line for line in reader]
            sensor_number = file_name[file_name.find('-')+1 : file_name.find('.')]
            temperature_humidity_data[sensor_number] = file_data[:number]

        return temperature_humidity_data


if __name__ == '__main__':
    read_data = ReadData("../data/filter_data","../data/pos/pos.csv")
    print read_data.get_pos_data()
    #print read_data.get_temperature_humidity_data(2)