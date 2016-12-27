#-*- coding:utf-8 -*-
import csv

class NumberToPos:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.table = {'10728412':'西北角地面',
                    '10728515':'西北角中',
                    '10728382':'西北角上',
                    '10728506':'西壁地面',
                    '10728402':'西壁中',
                    '10728400':'西壁上',
                    '10728435':'西陂地面',
                    '10728517':'西陂中',
                    '10728383':'西陂上',
                    '10728534':'窟中央祭坛',
                    '10728432':'窟中央中',
                    '10728401':'窟中央上',
                    '10728391':'东陂地面',
                    '10728437':'东陂中',
                    '10728525':'东陂上',
                    '10728399':'东南角地面',
                    '10728518':'东南角中',
                    '10728442':'东南角上',
                    '10728527':'甬道地面',
                    '10728390':'甬道中',
                    '10728405':'甬道上',
                    '10728419':'前室甬道口南侧地面',
                    '10728425':'前室甬道口南侧中',
                    '10728439':'前室甬道口南侧上',
                    '10728404':'前室中央地面',
                    '10728408':'前室中央中',
                    '10728522':'前室中央上中',
                    '10728396':'前室中央上',
                    '10728422':'前室东北角地面',
                    '10728507':'前室东北角中',
                    '10728513':'前室东北角上',
                    '10728387':'窟门南侧地面',
                    '10728385':'窟门南侧中',
                    '10728519':'窟门南侧上'
                    }

    def get_data(self):  #temp_hum=0时代表温度，1代表湿度
        file_data = []
        with open(self.data_file_path) as f:
            f_csv = csv.reader(f)
            start_count = 3
            for row in f_csv:
                file_data.append(row[:start_count])
                start_count += 1

        return file_data

    def convert(self, sensors):
        for item in sensors:
            print item,
        for item in sensors:
            print self.table[item],
        print


if __name__ == "__main__":
    ntp = NumberToPos("../data/result/layout_res_backup.csv")
    file_data = ntp.get_data()
    #print file_data

    for item in file_data:
        ntp.convert(item)
