#-*- coding:utf-8 -*-

from pykrige.ok import OrdinaryKriging
import numpy as np
import pykrige.kriging_tools as kt
import matplotlib.pyplot as plt
import matplotlib as mpl
import platform
import csv
import sys
sys.path.append("..")
from draw.draw_layout import drawLayout
from file_input_output.read_data import ReadData

class DrawHeatMap:
    def __init__(self):
        self.bottom = ['10728412', '10728506', '10728435', '10728391', '10728399', '10728527', '10728419', '10728404', '10728422', '10728387']
        self.mid = []
        self.up = []

    def getData(self, filtered_file_path, pos_file_path):
        read_data = ReadData(filtered_file_path, pos_file_path)
        temp_hum_data = read_data.get_temperature_humidity_data(1)
        pos_data = read_data.get_pos_data()
        print temp_hum_data
        print pos_data
        
        data = []
        for item in self.bottom:
            tmp = []
            tmp.append(float(pos_data[item][0]))
            tmp.append(float(pos_data[item][1]))
            tmp.append(float(temp_hum_data[item][0][0]))
            #print tmp
            #print pos_data[item][0], pos_data[item][1], temp_hum_data[item][0][0]
            #data.append( [int(pos_data[item][0])/10, int(pos_data[item][1])/10, float(temp_hum_data[item][0][0])] )
            data.append(tmp)

        data = np.array(data)
        print data

        x = range(0, 180, 5)
        y = range(0, 90, 5)

        gridx = []
        gridy = []
        for i in x:
            for j in y:
                gridx.append(i)
                gridy.append(j)

        gridx = np.array(gridx)
        gridy = np.array(gridy)

        OK = OrdinaryKriging(data[:, 0], data[:, 1], data[:, 2], variogram_model='linear',
                     verbose=False, enable_plotting=False)

        z, ss = OK.execute('points', gridx, gridy)

        print z



if __name__ == '__main__':
    dh = DrawHeatMap()
    dh.getData("../data/filter_data","../data/pos/pos.csv")

    # print read_data.get_temperature_humidity_data(1)
    # print read_data.get_pos_data()