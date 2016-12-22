#-*- coding:utf-8 -*-
import sys
sys.path.append("..")
from draw.draw_mean_error import DrawMeanError
from draw.draw_rmse import DrawRMSE
from draw.draw_pearson import DrawPearson
from draw.draw_average_mean_error import DrawAverageMeanError
from draw.draw_average_rmse import DrawAverageRMSE
from draw.draw_average_pearson import DrawAveragePearson

draw_mean_error = DrawMeanError("../data/result/MeanError.csv")
draw_mean_error.draw(0)
draw_mean_error.draw(1)

draw_rmse = DrawRMSE("../data/result/RMSE.csv")
draw_rmse.draw(0)
draw_rmse.draw(1)

draw_pearson = DrawPearson("../data/result/Pearson.csv")
draw_pearson.draw(0)
draw_pearson.draw(1)

draw_average_mean_error = DrawAverageMeanError("../data/result/MeanError.csv")
draw_average_mean_error.draw(0)
draw_average_mean_error.draw(1)

draw_average_rmse = DrawAverageRMSE("../data/result/RMSE.csv")
draw_average_rmse.draw(0)
draw_average_rmse.draw(1)


draw_average_pearson = DrawAveragePearson("../data/result/Pearson.csv")
draw_average_pearson.draw(0)
draw_average_pearson.draw(1)

print "done"