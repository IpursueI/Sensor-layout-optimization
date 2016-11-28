#-*- coding:utf-8 -*-

import math

class RMSE:
    """均方根误差"""
    def __init__(self, data):
        self.data = data

    def temperature_error(self):
        tmp = 0.0
        for item in self.data:
            tmp += (item[5]-item[4])*(item[5]-item[4])

        return math.sqrt(tmp/len(self.data))

    def humidity_error(self):
        tmp = 0.0
        for item in self.data:
            tmp += (item[7]-item[6])*(item[7]-item[6])

        return math.sqrt(tmp/len(self.data))

if __name__ == '__main__':
    rmse = RMSE()