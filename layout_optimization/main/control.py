#-*- coding:utf-8 -*-
import sys
sys.path.append("..")
from draw.draw_mean_error import DrawMeanError
from draw.draw_rmse import DrawRMSE
from draw.draw_pearson import DrawPearson
from draw.draw_average_mean_error import DrawAverageMeanError
from draw.draw_average_rmse import DrawAverageRMSE
from draw.draw_average_pearson import DrawAveragePearson
from draw.draw_barchart import DrawBarChart
from draw.draw_mean_barchart import DrawMeanBarChart

# draw_mean_error = DrawMeanError("../data/result/MeanError.csv")
# draw_mean_error.draw(0)
# draw_mean_error.draw(1)

# draw_rmse = DrawRMSE("../data/result/RMSE.csv")
# draw_rmse.draw(0)
# draw_rmse.draw(1)

# draw_pearson = DrawPearson("../data/result/Pearson.csv")
# draw_pearson.draw(0)
# draw_pearson.draw(1)

# draw_average_mean_error = DrawAverageMeanError("../data/result/MeanError.csv")
# draw_average_mean_error.draw(0)
# draw_average_mean_error.draw(1)

# draw_average_rmse = DrawAverageRMSE("../data/result/RMSE.csv")
# draw_average_rmse.draw(0)
# draw_average_rmse.draw(1)


# draw_average_pearson = DrawAveragePearson("../data/result/Pearson.csv")
# draw_average_pearson.draw(0)
# draw_average_pearson.draw(1)

# dbc = DrawBarChart()
# files = ["../data/result/MeanError.csv", "../data/result/RMSE.csv", "../data/result/Pearson.csv"]

# result_file_path = []

# for i in range(2):
#     for j in range(3):
#         dbc.draw(files[j], i, j)


# dmbc = DrawMeanBarChart()

# for i in range(2):
#     for j in range(3):
#         dmbc.draw(files[j], i, j)

# print "done"


import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


# example data
mu = 100  # mean of distribution
sigma = 15  # standard deviation of distribution
x = mu + sigma * np.random.randn(10000)
print x

num_bins = 10
# the histogram of the data
x= range(10)
n, bins, patches = plt.hist(x, num_bins, normed=1)
# add a 'best fit' line
# y = mlab.normpdf(bins, mu, sigma)
# plt.plot(bins, y, 'r--')
plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

# Tweak spacing to prevent clipping of ylabel
plt.subplots_adjust(left=0.15)
plt.show()