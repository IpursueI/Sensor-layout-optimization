#-*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import csv

class DrawPearson:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path

    def get_data(self, temp_hum):  #temp_hum=0时代表温度，1代表湿度
        file_data = []
        with open(self.data_file_path) as f:
            f_csv = csv.reader(f)
            for index,row in enumerate(f_csv):
                if index != 0 and index != 8 and index != 9:
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


    def draw(self, temp_hum):
        title = ['Temperature interpolation Pearson cross_validation','humidity interpolation Pearson cross_validation']

        majors = [['idw_temp','kriging_spherical_temp','kriging_linear_temp',
                    'kriging_power_temp','kriging_exponential_temp'],
                    ['idw_hum','kriging_spherical_hum','kriging_linear_hum',
                    'kriging_power_hum','kriging_exponential_hum']]

        y_offsets = {'idw_temp':0.5, 'kriging_spherical_temp':0.3, 'kriging_linear_temp':0.5,
                        'kriging_power_temp':0.6, 'kriging_gaussian_temp':0.5, 'kriging_exponential_temp':0.4,
                        'idw_hum':0.5, 'kriging_spherical_hum':0.4, 'kriging_linear_hum':0.6,
                        'kriging_power_hum':0.5, 'kriging_gaussian_hum':0.5, 'kriging_exponential_hum':0.55}

        file_data = self.get_data(temp_hum)
        color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c']

        fig, ax = plt.subplots(1, 1, figsize=(12, 14))

        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        plt.xlim(0,7.3)
        plt.ylim(-2, 2)

        for rank,column in enumerate(file_data):
            #print column
            line = plt.plot(range(7), column,lw=2.5,color=color_sequence[rank])

            y_pos = column[-1] - 0.5

            if majors[temp_hum][rank] in y_offsets:
                y_pos += y_offsets[majors[temp_hum][rank]]

            plt.text(6.2, y_pos, majors[temp_hum][rank], fontsize=14, color=color_sequence[rank])

        plt.title(title[temp_hum], fontsize=18, ha='center')

        plt.show()


if __name__ == '__main__':
    draw_pearson = DrawPearson("../data/result/Pearson.csv")
    #draw_pearson.draw(0)
    draw_pearson.draw(1)