#-*- coding:utf-8 -*-

import pygame,sys
import csv
from pygame.locals import *

class drawLayout:
    """利用pygame对variance.csv中的传感器布局进行绘制

    Attributes:
        WINDOWWIDTH: 窗口宽度
        WINDOWHEIGHT: 窗口高度

        AQUA - MYC: 颜色

        BGCOLOR: 背景色
        sensorPos: 传感器坐标

        sensorPos: 传感器编号做对应坐标，类型是字典
        variance: 从文件中读取的，每种传感器选择策略所对应的方差

        FPS: 程序运行时每秒的帧数
    """

    def __init__(self, posPath, pngPath, layoutData):
        """各个属性初始化
        """
        self.WINDOWWIDTH = 1250
        self.WINDOWHEIGHT = 800

        self.AQUA = (0, 255, 255)
        self.SILVER = (192, 192, 192)
        self.GRAY = (100, 100, 100)
        self.NAVYBLUE = ( 60, 60, 100)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = ( 0, 255, 0)
        self.BLUE = ( 0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.ORANGE = (255, 128, 0)
        self.PURPLE = (255, 0, 255)
        self.CYAN = ( 0, 255, 255)
        self.MYC = (107, 142, 35)

        self.BGCOLOR = self.SILVER

        self.sensorPng = pngPath

        self.sensorImg1 = pygame.image.load(self.sensorPng)

        self.sensorPos = self.readSensorPos(posPath)
        #self.variance = self.readVariance(variancePath)
        self.layoutData = layoutData



        self.FPS = 30 # frames per second setting
        self.fpsClock = pygame.time.Clock()
        

    def main(self):
        """控制整个程序的界面绘制
        """
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption('cave sensors layout')
        

        self.layoutCount = -1


        self.screen.fill(self.BGCOLOR)
        self.initDraw()
        self.drawSensorPos(False)

        while True:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    self.drawLayout()

            pygame.display.update()
            self.fpsClock.tick(self.FPS)


    def readSensorPos(self,filePath):
        """从文件中读取传感器的位置信息

        Args:
            filePath: 文件路径

        Returns:
            sensors: 一个字典，key为传感器编号，value为传感器的x,y坐标，以及传感器的高度编号,编号的取值为1-4
        """
        csvfile = file(filePath, 'rb')
        reader = csv.reader(csvfile)
        data = [line for line in reader]
        sensorPos = {}
        for item in data:
            sensorPos[item[0]] = (float(item[1])*0.6, 1000*0.6-float(item[2])*0.6, int(item[4]))
        #print sensorPos
        return sensorPos


    def initDraw(self):
        """初始化界面

        绘制界面背景色，洞窟的边界，以及按钮
        """
        self.screen.fill(self.BGCOLOR)

        pygame.draw.line(self.screen, self.GRAY, (0, 20), (600, 20), 15)
        pygame.draw.line(self.screen, self.GRAY, (600, 20), (600, 270), 15)
        pygame.draw.line(self.screen, self.GRAY, (600, 270), (700, 270), 15)
        pygame.draw.line(self.screen, self.GRAY, (700, 270), (700, 90), 15)
        pygame.draw.line(self.screen, self.GRAY, (700, 90), (1200, 90), 15)
        pygame.draw.line(self.screen, self.GRAY, (0, 20), (0, 650), 15)
        pygame.draw.line(self.screen, self.GRAY, (0, 650), (600, 650), 15)
        pygame.draw.line(self.screen, self.GRAY, (600, 650), (600, 480), 15)
        pygame.draw.line(self.screen, self.GRAY, (600, 480), (700, 480), 15)
        pygame.draw.line(self.screen, self.GRAY, (700, 480), (700, 590), 15)
        pygame.draw.line(self.screen, self.GRAY, (700, 590), (1200, 590), 15)


    #根据传感器位置进行绘制
    def drawSensorPos(self, drawSensorBar):
        """对传感器的位置进行绘制，包括传感器图标和一个1*4的矩形框

        Args:
            drawSensorBar:控制是否绘制1*4的矩形框
        """
        sensorPos = ((0,900),(0,460),(191.1,460),(461.1,460),(737.1,460),(920,0),(1010,460),(1100,290),(1450,460),(1800,740),(1800,300))
        sensorNarrowPos = [[item[0]*0.6, 1000*0.6-item[1]*0.6] for item in sensorPos]
        for item in sensorNarrowPos:
            self.screen.blit(self.sensorImg1, (item[0], item[1]))
            if drawSensorBar == True:
                pygame.draw.rect(self.screen, self.WHITE, (item[0]+60,item[1]-30, 25, 100))



    def drawLayout(self):
        """每按一次按钮，调用一次该函数，对整个界面重新绘制
        """

        self.initDraw()
        self.drawSensorPos(True)


        #根据选中的传感器，对其进行绘制，这里用各种颜色的1*1的矩形框代替

        for item in self.layoutData[:-1]:
            if self.sensorPos[item][2] == 1:
                pygame.draw.rect(self.screen, self.ORANGE, (self.sensorPos[item][0]+60,self.sensorPos[item][1]+45, 25, 25))
            elif self.sensorPos[item][2] == 2:
                pygame.draw.rect(self.screen, self.BLUE, (self.sensorPos[item][0]+60,self.sensorPos[item][1]+20, 25, 25))
            elif self.sensorPos[item][2] == 3:
                pygame.draw.rect(self.screen, self.PURPLE, (self.sensorPos[item][0]+60,self.sensorPos[item][1]-5, 25, 25))
            elif self.sensorPos[item][2] == 4:
                pygame.draw.rect(self.screen, self.CYAN, (self.sensorPos[item][0]+60,self.sensorPos[item][1]-30, 25, 25))

        #选择字体输出方差信息
        
        fontObj1 = pygame.font.Font('freesansbold.ttf', 25)

        textSurfaceObj = fontObj1.render("RMSE: %.2f"%(float(self.layoutData[-1])), True, self.WHITE)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (330, 150)
        self.screen.blit(textSurfaceObj, textRectObj)

        startX = 250
        for item in self.layoutData[:-1]:
            textSurfaceObj = fontObj1.render(item, True, self.WHITE)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (startX, 750)
            startX += 170
            self.screen.blit(textSurfaceObj, textRectObj)


if __name__ == '__main__':
    drawer = drawLayout('../data/pos/pos.csv', 'sensor.png', ['10728412', '10728402', '10728400', '10728435', '10728534', '12.33'])
    drawer.main()