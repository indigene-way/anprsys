#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
import re 
import uuid
import time
import math
import random
import datetime
from datetime import datetime

import sqlite3
from PyQt5.QtSql import *

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#============================================================================================================DATA BASE
conn = sqlite3.connect('db.db')
# os.system("icacls db.db /grant *S-1-1-0:(D,WDAC)")	
query = conn.cursor()

#===========================================================================Vehicules 
# query.execute("DROP TABLE Cars")
try:
    query.execute("SELECT id FROM Cars ORDER BY id DESC")

except:
    conn.execute("""CREATE TABLE Cars (
					id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
					car_mat VARCHAR(50) ,
					car_date DATE,
					car_date_depart DATE,
					car_arrive TIME(0),
					car_depart TIME(0))""")

    
# =============UI CLASS Widget ANPR		
qtANPRW= "DESIGN/WIDGETS/AnprWidget.ui"
Ui_AnprWidget, QtBaseClass = uic.loadUiType(qtANPRW)	
class AnprWidget(QDialog, Ui_AnprWidget):#EDIT : MODIF Product Name,Price DIALOG
	
    def __init__(self):
        QDialog.__init__(self)
        Ui_AnprWidget.__init__(self)
        self.setupUi(self)	 
        
# =============UI CLASS Widget PARK		
qtANPRP= "DESIGN/WIDGETS/AnprParked.ui"
Ui_AnprPark, QtBaseClass = uic.loadUiType(qtANPRP)	
class AnprPark(QDialog, Ui_AnprPark):#EDIT : MODIF Product Name,Price DIALOG
	
    def __init__(self):
        QDialog.__init__(self)
        Ui_AnprPark.__init__(self)
        self.setupUi(self)	  
        
# =============UI CLASS Widget HISTORY		
qtANPRH= "DESIGN/WIDGETS/AnprHistory.ui"
AnprHistory, QtBaseClass = uic.loadUiType(qtANPRH)	
class AnprHist(QDialog, AnprHistory):#EDIT : MODIF Product Name,Price DIALOG
	
    def __init__(self):
        QDialog.__init__(self)
        AnprHistory.__init__(self)
        self.setupUi(self)	

# =============GLOBAL TIME VARIABLES
date = time.strftime("%Y-%m-%d")
dateIndicator = time.strftime("%Y %m %d")

matList=["01 CC 1A 0001","DZI7 YXR","SN66 XMZ","LR33 TEE","01505 111 16"\
,"SKIP GAS","P3RV P","G526 JHD","GRAIG","LSI5 EBC"]       

# =============UI CLASS DIALOG		
qtANPR= "DESIGN/WIDGETS/ANPRGUI.ui"
Ui_Anpr, QtBaseClass = uic.loadUiType(qtANPR)	
class Anpr(QDialog, Ui_Anpr):#EDIT : MODIF Product Name,Price DIALOG
	
    def __init__(self):
        QDialog.__init__(self)
        Ui_Anpr.__init__(self)
        self.setupUi(self)
        
        self.show()
        self.setWindowTitle("ANPR System.")
        
        #INSTANCES
        self.Hist = AnprHist()
        self.Park = AnprPark()
        self.Anpr = AnprWidget()
        
        self.dockWidget.setWidget(self.Anpr)
        
        self.dateTime = time.strftime("%d-%m-%Y      %H:%M:%S")
        # self.now = time.strftime("%H:%M:%S")
        now = datetime.now()
        self.current_time = now.strftime("%H:%M:%S")
        
        self.Anpr.daterIndicator.setText(dateIndicator)
        # self.timeIndicator.setText(self.current_time)
        
        self.TableWidgetInit()#TABLE WIDGET DEFAULT
        
        #SIGNAL capture
        self.Anpr.capture.clicked.connect(self.CaptureMat)
        #SIGNAL menu
        self.menuMain.clicked.connect(self.menu1)
        self.menuPark.clicked.connect(self.menu2)
        self.menuData.clicked.connect(self.menu3)
        
        #SIGNAL Buttons
        self.Anpr.newCar.clicked.connect(self.NewCar)
        
        #SIGNAL HISTORY BUTTONS
        self.Hist.matFindHist.clicked.connect(self.Finder)
        self.Hist.dateFindHist.clicked.connect(self.Finder)
        
        #SIGNAL HISTORY BUTTONS
        self.Park.depart.clicked.connect(self.Depart)
        self.Park.matFindPark.clicked.connect(self.Finder)
        self.Park.dateFindPark.clicked.connect(self.Finder)
        
        #INIT TABLE WIDGETS/ANPR
        self.car = 0
        
    def TableWidgetInit(self):
        #CLEAN TABLE WIDGET
        self.Anpr.tableWidget.clear()
        self.Anpr.tableWidget.clearContents()
        self.Anpr.tableWidget.setRowCount(0)
        
        self.Anpr.tableWidget.setColumnCount(4)
        self.Anpr.tableWidget.setColumnWidth(0, 200)
        self.Anpr.tableWidget.setColumnWidth(1, 200)
        self.Anpr.tableWidget.setColumnWidth(2, 200)
        self.Anpr.tableWidget.setColumnWidth(3, 200)
        
        self.Anpr.tableWidget.setHorizontalHeaderLabels(['Date', 'Heure arrivée', 'Matricule','Heure départ'])
        self.header = self.Anpr.tableWidget.horizontalHeader()
        self.header.setDefaultAlignment(Qt.AlignHCenter)
    
    def menu1(self):#ANPR SYS
        self.dockWidget.setWidget(self.Anpr)
        
        self.indicator.setText("ANPR System")
        icon = "IMAGES/Icons/menuSquares.png"
        self.iconIndicator.setIcon(QIcon(icon))
        
        #GETTING DATA
        self.cur = query
        self.cur.execute("SELECT car_date,car_arrive,car_mat FROM Cars WHERE car_date = '{0}' AND id=(SELECT max(id) FROM Cars) \
        ORDER BY id DESC".format(str(dateIndicator)))
        # lastCar=str(query.fetchone()).strip("(',')")
        
        #CLEAN TABLE WIDGET AND PRINT DATA
        self.Anpr.tableWidget.clear()
        self.Anpr.tableWidget.clearContents()
        self.Anpr.tableWidget.setRowCount(0)
        
        self.Anpr.tableWidget.setColumnCount(3)
        self.Anpr.tableWidget.setColumnWidth(0, 257)
        self.Anpr.tableWidget.setColumnWidth(1, 257)
        self.Anpr.tableWidget.setColumnWidth(2, 257)
        
        self.Anpr.tableWidget.setHorizontalHeaderLabels(['Date', 'Heure arrivée', 'Matricule'])
        self.header = self.Anpr.tableWidget.horizontalHeader()
        self.header.setDefaultAlignment(Qt.AlignHCenter)
        
        for row, form in enumerate(query):
            self.Anpr.tableWidget.insertRow(row)
            for column, item in enumerate(form):
                #print(str(item))
                self.Anpr.tableWidget.setItem(row, column,QTableWidgetItem(str(item)))
    
    def menu2(self):#PARKED CARS
        self.dockWidget.setWidget(self.Park)
        self.Park.datePark.setDisplayFormat("yyyy MM dd")
        
        self.indicator.setText("Places Occupées")
        icon = "IMAGES/Icons/parking.png"
        self.iconIndicator.setIcon(QIcon(icon))
        
        # GETTING DATA
        self.cur = query
        self.cur.execute("SELECT car_date,car_arrive,car_mat FROM Cars WHERE car_depart IS NULL \
        ORDER BY id DESC")
        
        # CLEAN TABLE WIDGET AND PRINT DATA
        self.Park.parkTabWidget.clear()
        self.Park.parkTabWidget.clearContents()
        self.Park.parkTabWidget.setRowCount(0)
        
        self.Park.parkTabWidget.setColumnCount(3)
        self.Park.parkTabWidget.setColumnWidth(0, 257)
        self.Park.parkTabWidget.setColumnWidth(1, 257)
        self.Park.parkTabWidget.setColumnWidth(2, 257)
        
        self.Park.parkTabWidget.setHorizontalHeaderLabels(['Date', 'Heure arrivée', 'Matricule'])
        self.header = self.Park.parkTabWidget.horizontalHeader()
        self.header.setDefaultAlignment(Qt.AlignHCenter)
        
        for row, form in enumerate(self.cur):
            self.Park.parkTabWidget.insertRow(row)
            for column, item in enumerate(form):
                self.Park.parkTabWidget.setItem(row, column,QTableWidgetItem(str(item)))
    
    def menu3(self):
        self.dockWidget.setWidget(self.Hist)
        self.Hist.dateHist.setDisplayFormat("yyyy MM dd")
        self.indicator.setText("Historique")
        icon = "IMAGES/Icons/database.png"
        self.iconIndicator.setIcon(QIcon(icon))
        
        # GETTING DATA
        self.cur = query
        self.cur.execute("SELECT car_date,car_arrive,car_mat,car_depart,car_date_depart FROM Cars WHERE car_depart IS NOT NULL ORDER BY id DESC")
        
        #CLEAN TABLE WIDGET
        self.Hist.histTabWidget.clear()
        self.Hist.histTabWidget.clearContents()
        self.Hist.histTabWidget.setRowCount(0)
        
        self.Hist.histTabWidget.setColumnCount(5)
        self.Hist.histTabWidget.setColumnWidth(0, 155)
        self.Hist.histTabWidget.setColumnWidth(1, 155)
        self.Hist.histTabWidget.setColumnWidth(2, 155)
        self.Hist.histTabWidget.setColumnWidth(3, 155)
        self.Hist.histTabWidget.setColumnWidth(4, 155)
        
        self.Hist.histTabWidget.setHorizontalHeaderLabels(['Date arrivée', 'Heure arrivée', 'Matricule','Heure départ','Date départ'])
        self.header = self.Hist.histTabWidget.horizontalHeader()
        self.header.setDefaultAlignment(Qt.AlignHCenter)
        
        for row, form in enumerate(self.cur):
            self.Hist.histTabWidget.insertRow(row)
            for column, item in enumerate(form):
                self.Hist.histTabWidget.setItem(row, column,QTableWidgetItem(str(item)))
    
    def NewCar(self):
        self.car = random.randint(1, 10)
    
        self.imgCar = QtGui.QPixmap("IMAGES/Cars/car"+str(self.car)+".png") 
        self.Anpr.matWidget.clear()
        self.Anpr.carWidget.setPixmap(QtGui.QPixmap(self.imgCar)) 
        self.Anpr.noIndicator.clear()
        
    def CaptureMat(self):
        if self.car != 0 :
            #IMAGES SETTINGS
            self.imgMat = QtGui.QPixmap("IMAGES/Cars/"+str(self.car)+".png") 
            self.Anpr.matWidget.setPixmap(QtGui.QPixmap(self.imgMat))
            
            #ACTUAL TIME SETTINGS
            self.hour = int(time.strftime("%H"))
            self.min = int(time.strftime("%M"))
            self.sec = int(time.strftime("%S"))
           
            #INDICATORS 
            self.Anpr.timeIndicator.setDisplayFormat("hh:mm:ss")
            self.Anpr.timeIndicator.setTime(QtCore.QTime(int(self.hour),int(self.min), int(self.sec)))
            
            self.Anpr.matIndicator.setText(matList[self.car - 1])
            self.Anpr.noIndicator.clear()
            
            #CLEAN TABLE WIDGET AND PRINT DATA
            self.Anpr.tableWidget.clear()
            self.Anpr.tableWidget.clearContents()
            self.Anpr.tableWidget.setRowCount(0)
            
            self.Anpr.tableWidget.setColumnCount(3)
            self.Anpr.tableWidget.setColumnWidth(0, 257)
            self.Anpr.tableWidget.setColumnWidth(1, 257)
            self.Anpr.tableWidget.setColumnWidth(2, 257)
            
            self.Anpr.tableWidget.setHorizontalHeaderLabels(['Date', 'Heure arrivée', 'Matricule'])
            self.header = self.Anpr.tableWidget.horizontalHeader()
            self.header.setDefaultAlignment(Qt.AlignHCenter)
            
            self.rowPosition = self.Anpr.tableWidget.rowCount()
            self.Anpr.tableWidget.insertRow(self.rowPosition)
            
            self.Anpr.tableWidget.setSortingEnabled(True)
            self.Anpr.tableWidget.setItem(self.rowPosition , 0, QTableWidgetItem(dateIndicator))
            self.Anpr.tableWidget.setItem(self.rowPosition , 1, QTableWidgetItem(str(self.current_time)))
            self.Anpr.tableWidget.setItem(self.rowPosition , 2, QTableWidgetItem(str(matList[self.car - 1])))
            
            #BINDING DATA
            timer = str(int(self.Anpr.timeIndicator.time().hour())) +":"+ str(int(self.Anpr.timeIndicator.time().minute())) +\
            ":"+ str(int(self.Anpr.timeIndicator.time().second()))
            
            query.execute("INSERT INTO Cars (car_mat,car_date,car_arrive)\
            values('{0}','{1}','{2}');".format(str(matList[self.car - 1]), dateIndicator, str(self.current_time)))
            conn.commit()
        else :
            self.Anpr.noIndicator.setText("Aucun matricule détecté")

    def Finder(self):
        sender = self.sender()
        
        if sender == self.Hist.dateFindHist :
            date = self.Hist.dateHist.text()
            if date != "":
                # GETTING DATA SELECT 
                self.cur = query
                self.cur.execute("SELECT car_date,car_arrive,car_mat,car_depart,car_date_depart FROM Cars WHERE car_date = '{0}' AND car_depart IS NOT NULL \
                ORDER BY id DESC".format(str(date)))
        
                #CLEAN TABLE WIDGET
                self.Hist.histTabWidget.clear()
                self.Hist.histTabWidget.clearContents()
                self.Hist.histTabWidget.setRowCount(0)
                
                self.Hist.histTabWidget.setColumnCount(5)
                self.Hist.histTabWidget.setColumnWidth(0, 155)
                self.Hist.histTabWidget.setColumnWidth(1, 155)
                self.Hist.histTabWidget.setColumnWidth(2, 155)
                self.Hist.histTabWidget.setColumnWidth(3, 155)
                self.Hist.histTabWidget.setColumnWidth(4, 155)
                
                self.Hist.histTabWidget.setHorizontalHeaderLabels(['Date arrivée', 'Heure arrivée', 'Matricule','Heure départ','Date départ'])
                self.header = self.Hist.histTabWidget.horizontalHeader()
                self.header.setDefaultAlignment(Qt.AlignHCenter)
                
                for row, form in enumerate(self.cur):
                    self.Hist.histTabWidget.insertRow(row)
                    for column, item in enumerate(form):
                        self.Hist.histTabWidget.setItem(row, column,QTableWidgetItem(str(item)))
                
        if sender == self.Hist.matFindHist :
            mat = self.Hist.matHist.text()
            if mat != "":
                # GETTING DATA
                self.cur = query
                self.cur.execute("SELECT car_date,car_arrive,car_mat,car_arrive,car_date_depart FROM Cars WHERE car_mat = '{0}' AND car_depart IS NOT NULL \
                ORDER BY id DESC".format(str(mat)))
        
                #CLEAN TABLE WIDGET
                self.Hist.histTabWidget.clear()
                self.Hist.histTabWidget.clearContents()
                self.Hist.histTabWidget.setRowCount(0)
                
                self.Hist.histTabWidget.setColumnCount(5)
                self.Hist.histTabWidget.setColumnWidth(0, 155)
                self.Hist.histTabWidget.setColumnWidth(1, 155)
                self.Hist.histTabWidget.setColumnWidth(2, 155)
                self.Hist.histTabWidget.setColumnWidth(3, 155)
                self.Hist.histTabWidget.setColumnWidth(4, 155)
                
                self.Hist.histTabWidget.setHorizontalHeaderLabels(['Date arrivée', 'Heure arrivée', 'Matricule','Heure départ','Date départ'])
                self.header = self.Hist.histTabWidget.horizontalHeader()
                self.header.setDefaultAlignment(Qt.AlignHCenter)
                
                for row, form in enumerate(self.cur):
                    self.Hist.histTabWidget.insertRow(row)
                    for column, item in enumerate(form):
                        self.Hist.histTabWidget.setItem(row, column,QTableWidgetItem(str(item)))
                
        if sender == self.Park.dateFindPark :
            date = self.Park.datePark.text()
            if date != "":
                # GETTING DATA
                self.cur = query
                self.cur.execute("SELECT car_date,car_arrive,car_mat FROM Cars WHERE car_date = '{0}' AND car_depart IS NULL \
                ORDER BY id DESC".format(str(date)))
                
                # CLEAN TABLE WIDGET AND PRINT DATA
                self.Park.parkTabWidget.clear()
                self.Park.parkTabWidget.clearContents()
                self.Park.parkTabWidget.setRowCount(0)
                
                self.Park.parkTabWidget.setColumnCount(3)
                self.Park.parkTabWidget.setColumnWidth(0, 257)
                self.Park.parkTabWidget.setColumnWidth(1, 257)
                self.Park.parkTabWidget.setColumnWidth(2, 257)
                
                self.Park.parkTabWidget.setHorizontalHeaderLabels(['Date', 'Heure arrivée', 'Matricule'])
                self.header = self.Park.parkTabWidget.horizontalHeader()
                self.header.setDefaultAlignment(Qt.AlignHCenter)
                
                for row, form in enumerate(self.cur):
                    self.Park.parkTabWidget.insertRow(row)
                    for column, item in enumerate(form):
                        self.Park.parkTabWidget.setItem(row, column,QTableWidgetItem(str(item)))
                
        if sender == self.Park.matFindPark :
            mat = self.Park.matPark.text()
            if mat != "":
                # GETTING DATA
                self.cur = query
                self.cur.execute("SELECT car_date,car_arrive,car_mat FROM Cars WHERE car_mat = '{0}' AND car_depart IS NULL \
                ORDER BY id DESC".format(str(mat)))
                
                # CLEAN TABLE WIDGET AND PRINT DATA sender
                self.Park.parkTabWidget.clear()
                self.Park.parkTabWidget.clearContents()
                self.Park.parkTabWidget.setRowCount(0)
                
                self.Park.parkTabWidget.setColumnCount(3)
                self.Park.parkTabWidget.setColumnWidth(0, 257)
                self.Park.parkTabWidget.setColumnWidth(1, 257)
                self.Park.parkTabWidget.setColumnWidth(2, 257)
                
                self.Park.parkTabWidget.setHorizontalHeaderLabels(['Date', 'Heure arrivée', 'Matricule'])
                self.header = self.Park.parkTabWidget.horizontalHeader()
                self.header.setDefaultAlignment(Qt.AlignHCenter)
                
                for row, form in enumerate(self.cur):
                    self.Park.parkTabWidget.insertRow(row)
                    for column, item in enumerate(form):
                        self.Park.parkTabWidget.setItem(row, column,QTableWidgetItem(str(item)))
 
    def Depart(self):
        dateDepart = time.strftime("%Y %m %d")
        nowTime = datetime.now()
        current_time = nowTime.strftime("%H:%M:%S")
        #==========HOVER ONN TITLE
        rowPosition = self.Park.parkTabWidget.rowCount()
        index = self.Park.parkTabWidget.currentRow()
        
        carDate = self.Park.parkTabWidget.item(index,0).text()
        carArrive = self.Park.parkTabWidget.item(index,1).text()
        carMat = self.Park.parkTabWidget.item(index,2).text()
        
        query.execute("UPDATE Cars SET car_depart = '{0}', car_date_depart='{1}' WHERE car_arrive = '{2}' AND car_date = '{3}' AND car_mat = '{4}'"\
        .format(str(current_time),str(dateDepart),str(carArrive),str(carDate),str(carMat)))
        conn.commit()
        self.menu2()
        
if __name__ == '__main__':
    
	app = QApplication(sys.argv)
	ex = Anpr()
    
	sys.exit(app.exec_())