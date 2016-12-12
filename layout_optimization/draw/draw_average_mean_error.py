#-*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import csv

class DrawAverageMeanError:
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
        title = ['Temperature interpolation average mean error cross_validation','humidity interpolation average mean error cross_validation']

        majors = [['idw_temp','kriging_spherical_temp','kriging_linear_temp',
                    'kriging_power_temp','kriging_exponential_temp'],
                    ['idw_hum','kriging_spherical_hum','kriging_linear_hum',
                    'kriging_power_hum','kriging_exponential_hum']]

        y_offsets = {'idw_temp':0.5, 'kriging_spherical_temp':0.5, 'kriging_linear_temp':0.4,
                        'kriging_power_temp':0.5, 'kriging_gaussian_temp':0.5, 'kriging_exponential_temp':0.5,
                        'idw_hum':0.5, 'kriging_spherical_hum':0.4, 'kriging_linear_hum':0.5,
                        'kriging_power_hum':0.5, 'kriging_gaussian_hum':0.5, 'kriging_exponential_hum':0.5}

        file_data = self.get_data(temp_hum)
        color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c']

        fig, ax = plt.subplots(1, 1, figsize=(12, 14))

        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        ax.set_xticks(range(5))
        ax.set_xticklabels(majors[temp_hum])

        plt.xlim(-0.5,4.5)
        if temp_hum == 0:
            plt.ylim(-0.1, 0.1)
        elif temp_hum == 1:
            plt.ylim(-0.2,0.1)

        plt.plot(range(5), [0] * 5, '--',lw=1.5, color='black', alpha=0.3)

        line = plt.plot(range(5), file_data,lw=2.5,color=color_sequence[0])

        y_pos = file_data[-1] - 0.5

        #plt.text(5.2, y_pos, "average RMSE", fontsize=14, color=color_sequence[0])

        plt.title(title[temp_hum], fontsize=18, ha='center')

        plt.show()


if __name__ == '__main__':
    draw_average_mean_error = DrawAverageMeanError("../data/result/MeanError.csv")
    draw_average_mean_error.draw(0)
    draw_average_mean_error.draw(1)