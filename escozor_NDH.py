#!/usr/bin/python3
'''
    File Name:  escozor_NDH.py
    Description:This file contains Ui part and by using instances of Haversine and Gps class of the supporting file,
                every 50ms it takes GPS snapshot and measure the current Liner distance from the 5 Hazardous ares.
                Based on the threshold value (the value less than that we want to have visual alarm) It will display 
                visual alarm (changing a screen with the message having information of total accident happend in past
                for the next intersection).

                This is contineous process and Normal (Good to go ahead) screen will get back as soon as vehicle 
                goes far from the hazardous instersection/area.

    Author:     Nirav Jasani (Main algorithm development and final Integration)
                Dhaval Patidar (GUI part)
                Harleen Kaur (Code optimization)
    Date:       Versin 1.0 (March-08-2020):
                    -GUI part developed in Tkinter.
                    -Got GUI working standalone based as expected.
                Version 2.0 (March-18-2020):
                    -Implementation GUI in PyQt5 started.
                    -Timer implematation done
                    -Integration of Haversine class and Gps class done.

'''

#----------------Importing Qt5 Modules from PyQt5--------------------------------------------#
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * #pyqtSignal,QObject,QTimer

#------------Importing classes---------------------------------------------------------------#
from haversine import Haversine
from gps import Gps

#----------Importing Time module------------------------------------------------------------#
import time 

'''
    Providing 5 seconds delay before starting application to monitor incase any issue or bug occures or not
'''
time.sleep(5)

'''
    Ui class:
        set up mainUI, Images and MessageBoxe
'''

class Ui_MainWindow():

    def __init__(self):
        self.a=Gps()
        self.setupUi(MainWindow)
    '''
        Setting up UI
    '''
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("normal.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.msgBox = QtWidgets.QLabel(self.centralwidget)
        self.msgBox.setGeometry(QtCore.QRect(50,10,711,31))
        font= QtGui.QFont()
        font.setPointSize(20)
        self.msgBox.setFont(font)
        self.msgBox.setStyleSheet("color:rgb(255,255,255)")
        self.msgBox.setTextFormat(QtCore.Qt.AutoText)
        self.msgBox.setScaledContents(True)
        self.msgBox.setObjectName("msgBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    '''
        very 50ms this method will get the current distance from the Hazardous area/intersection
    '''
    def getDistance(self):
        self.temp=self.a.getLocation()# stores current location in self.temp
        threshold=900.0000 #This is the threshold value in meter that user wants to have visual alarm before he/she enters into the Hazardous area.
        data = [500,600,700,800,900,1000]#Random numers describing the number of accident occured in listed 5 intersections accordingly

        if self.temp:
            self.distanceHB = Haversine(self.temp,Haversine.HomerBlock)#stores current distance from Homerwatson/Block line intersection
            self.distanceFW = Haversine(self.temp,Haversine.FairwayWilson)#stores current distance from Fairway/Wilson intersection
            self.distanceHBishop = Haversine(self.temp,Haversine.HasplarBishop)#stores current distance from Hasplar/Bishop intersectiomn
            self.distanceHM = Haversine(self.temp,Haversine.HasplarMaple)#stores current distance from haslpar/maple intersection
            self.distanceHQ = Haversine(self.temp,Haversine.HasplarQueen)#stores current distance from hasplar/Queen intersection
            '''
                Storing all the distance in one dictionary
            '''
            self.dict1= {"Homer Block":self.distanceHB.m(),"Fairview Wilson":self.distanceFW.m(),"Hasplar Bishop":self.distanceHBishop.m(),\
                    "Hasplar Maple":self.distanceHM.m(),"Hasplar Queen":self.distanceHQ.m()}
            print("_____________________________________________")


            '''
                conditioning for visual alarm 
            '''
            if self.distanceHB.m() < threshold or self.distanceFW.m() < threshold or self.distanceHBishop.m() < threshold or \
                    self.distanceHM.m() < threshold or self.distanceHQ.m() <threshold:
               print("\nHazardous Area Ahead\n")
               self.label.setPixmap(QtGui.QPixmap("warning.png"))
               if self.distanceHB.m() <  threshold:
                   self.msgBox.setText(str(data[0])+" "+"Accidents happend at the next intersection")
               elif self.distanceFW.m() <threshold:
                   self.msgBox.setText(str(data[1])+" "+"Accidents happend at the next intersection")
               elif self.distanceHBishop.m() < threshold:
                   self.msgBox.setText(str(data[2])+" "+"Accidents happend at the next intersection")
               elif self.distanceHM.m() <threshold:
                   self.msgBox.setText(str(data[3])+" "+"Accidents happend at the next intersection")
               elif self.distanceHQ.m() < threshold:
                   self.msgBox.setText(str(data[4])+" "+"Accidents happend at the next intersection") 
              
            else:
                print("\n you are safe\n")
                self.label.setPixmap(QtGui.QPixmap("normal.png"))
                self.msgBox.setText("You are good to go !!!")

            '''
                Printing all Keys and values from the disctionary on the shell
            '''
            for x in self.dict1:
                print(self.dict1,"\n")
                if self.dict1[x]<threshold:
                    print(x,"->",self.dict1[x])
            


'''
    Program starts from here and making some instances of QTimer(), QrWidgets() and  Ui_MainWindow() Classes.
    By generating 50 ms timer. After every 50 ms time, getDistance() method of the Ui_MainWidow() class gets called.
    So every 50 ms , we are getting GPS co-ordinates and using Haversine algorithm we are calculating current distance here.
    Based on the current distance we have put some conditioning for displaying visual effects on the screen.
'''
if __name__ == "__main__":
    import sys
    timer1 = QTimer()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    timer1.timeout.connect(ui.getDistance)
    timer1.start(50)
    sys.exit(app.exec_())
    
