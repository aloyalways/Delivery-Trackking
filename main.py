from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import sys
import time
import threading
import os
import traceback
import json
import shutil
import weakref
import csv
from decimal import Decimal
import base64
from functools import partial
import queue
import asyncio
from typing import Optional
import math
from collections import namedtuple
import numpy as np
import smtplib

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *


#Creating main window
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Delivering & Tracking'
        self.setWindowTitle(self.title)

        self.tab_widget = MyTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.showFullScreen()


#Creating the tab widgets
class MyTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        #Initialize tab screen
        self.tabs = QTabWidget()
        self.map_tab = Maps()
        self.address_tab = Addresses()
        self.guy_tab=DeliveryGuys()

        self.map_tab.clicked_start.connect(self.address_tab.add_table)
        self.map_tab.clicked_show.connect(self.guy_tab.add_map)
        self.tabs.resize(300,200)

        #Add tabs
        self.tabs.addTab(self.map_tab,QIcon("./icons and images/tab_map.png"), ('Home'))
        self.tabs.addTab(self.address_tab,QIcon("./icons and images/tab_addresses.png"), ('Addresses'))
        self.tabs.addTab(self.guy_tab,QIcon("./icons and images/tab_guy.png"), ('Delivery Guys'))

        #Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


#Creating the first tab
class Maps(QWidget):
    clicked_start = pyqtSignal(float, str)
    clicked_show = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.gif_animation()
        self.startButton()

    #Adding the background GIF
    def gif_animation(self):
        self.movie = QMovie('./icons and images/giphy.gif', QByteArray(), self)

        size = self.movie.scaledSize()

        self.movie_screen = QLabel()

        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)

        self.setLayout(main_layout)

        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()

        self.setGeometry(50,50,100,100)
        self.setMinimumSize(10,10)

    #Resizing the GIF to the size of the window
    def resizeEvent(self, event):
        rect = self.geometry()
        size = QSize(min(rect.width(), rect.height()), min(rect.width(), rect.height()))

        movie = self.movie_screen.movie()
        movie.setScaledSize(size)
        
    def paintEvent(self, e):
        #heading left
        qp_hleft = QPainter()
        qp_hleft.begin(self)

        pen = QPen(Qt.black)
        pen.setWidth(2)
        qp_hleft.setPen(pen)        

        font = QFont()
        font.setFamily('Times')
        font.setBold(True)
        font.setPointSize(30)
        qp_hleft.setFont(font)

        qp_hleft.drawText(e.rect(), Qt.AlignLeft,"\n     What is D&T ?")

        qp_hleft.end()
        
        #Heading right
        qp_hright = QPainter()
        qp_hright.begin(self)

        pen = QPen(Qt.black)
        pen.setWidth(2)
        qp_hright.setPen(pen)        

        font = QFont()
        font.setFamily('Times')
        font.setBold(True)
        font.setPointSize(30)
        qp_hright.setFont(font)

        qp_hright.drawText(e.rect(), Qt.AlignRight,"\nInstruction:        ")

        qp_hright.end()
        
        #information left
        qp_left = QPainter()
        qp_left.begin(self)
        
        self.text = "\n\n\n\n\n    It is an application where all\n\n the information of the customers\n\n   is extracted and based on these\n\n data a planned route is generated.\n\n   For instance, if a delivery guy\n\n   is given the task of delivering\n\n    30 items in a day. So, where\n\n   he/she should deliver first and\n\n on what basis. This is where our\n\n   system comes in, which gives\n\n the route with all the information\n\n   texted to the delivery person."

        pen = QPen(Qt.black)
        pen.setWidth(2)
        qp_left.setPen(pen)        

        font = QFont()
        font.setFamily('Times')
        font.setBold(False)
        font.setPointSize(20)
        qp_left.setFont(font)

        qp_left.drawText(e.rect(), Qt.AlignLeft, self.text)

        qp_left.end()
        
        #information right
        qp_right = QPainter()
        qp_right.begin(self)
        
        self.text = "\n\n\n\n\nB y  c l i c k i n g  S T A R T  -> \n\n•   After   clicking   the   START\n\n button ,    a    list    of    all    the\n\ninformation about the customers \n\narranged according to a perfectly \n\nplanned    route    is    generated.\n\n•    The         list         can         be\n\nseen     under     Addresses     tab.\n\n\n\nB y    c l i c k i n g    S H O W ->\n\n•  An    animated    map    version\n\nof     list     is     generated     by\n\nclicking  on  the  SHOW  button.\n\n•  This   animated   map   can   be\n\nseen  under  Delivery  Guy  tab."

        pen = QPen(Qt.black)
        pen.setWidth(2)
        qp_right.setPen(pen)        

        font = QFont()
        font.setFamily('Times')
        font.setBold(False)
        font.setPointSize(20)
        qp_right.setFont(font)

        qp_right.drawText(e.rect(), Qt.AlignRight, self.text)

        qp_right.end()


    #Push button at the center
    def startButton(self):
        self.button1 = QPushButton("Start", self)
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap("./icons and images/start_icon.png"))
        self.button1.setIcon(self.icon)
        self.button1.move(655, 390)
        self.button1.clicked.connect(self.table)
        
        self.button2 = QPushButton("Show", self)
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap("./icons and images/show_icon.png"))
        self.button2.setIcon(self.icon)
        self.button2.move(655, 415)
        self.button2.clicked.connect(self.clicked_show)
        self.show()

    @pyqtSlot()
    def table(self):
        self.button1.setEnabled(False)

        with open('orders.json') as f:
            data=json.load(f)
        rowcol = 0
        latarr=[]
        longarr=[]
        for orders in data['orders']:
            latarr.append(orders['Latitude'])
            longarr.append(orders['Longitude'])
            rowcol+=1

        #Distance between geographical points on the surface of the Earth
        def distance(origin, destination):
            lat1, lon1 = origin
            lat2, lon2 = destination
            radius = 6371

            dlat = math.radians(lat2-lat1)
            dlon = math.radians(lon2-lon1)
            a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            d = radius * c

            return d

        d_matrix = []

        #Creating the distance matrix
        for i in range(rowcol):
            a =[]
            for j in range(rowcol):
                lat1=float(latarr[i])
                long1=float(longarr[i])
                lat2=float(latarr[j])
                long2=float(longarr[j])

                d = distance((lat1, long1), (lat2, long2))
                a.append(d)
            d_matrix.append(a)

        data = {}
        data['distance_matrix'] = d_matrix
        data['num_vehicles'] = 1
        data['depot'] = 0

        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                               data['num_vehicles'], data['depot'])

        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        assignment = routing.SolveWithParameters(search_parameters)

        if assignment:
            #Finding the best route
            print('Average travel: {} Kilometres'.format(float(assignment.ObjectiveValue())*1.6))
            index = routing.Start(0)
            print("Route:")
            plan_output = ''
            route_distance = 0

            while not routing.IsEnd(index):
                plan_output += '{}'.format(manager.IndexToNode(index))
                previous_index = index
                index = assignment.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)

            plan_output += '{}'.format(manager.IndexToNode(index))

            #Creating the map
            indore_map = folium.Map(location = [22.712215,75.869869], zoom_start = 12.5 )

            with open('orders.json') as f:
                data=json.load(f)

            mainicon = folium.features.CustomIcon('./icons and images/main_marker.png', icon_size=(40,40))
            for orders in data['orders']:
                if orders['Name'] == "Main":
                    folium.Marker([orders['Latitude'],orders['Longitude']], popup = (orders['Name'] + '<br>' + orders['Mobile No.'] + '<br>' + orders['Address']), tooltip = "Click for more information.", icon = mainicon).add_to(indore_map)
                    continue
                folium.Marker([orders['Latitude'],orders['Longitude']], popup = (orders['Name'] + '<br>' + orders['Mobile No.'] + '<br>' + orders['Address']), tooltip = "Click for more information.").add_to(indore_map)

            latarr = []
            longarr = []
            for i in plan_output:
                for orders in data['orders']:
                    if i == orders['S No.']:
                        latarr.append(float(orders['Latitude']))
                        longarr.append(float(orders['Longitude']))
                        break

        raw = open('test.txt', "r+")
        contents = raw.read().split("\n")
        raw.seek(0)
        raw.truncate()
        raw.write("0681743250")

        self.clicked_start.emit(45.6, "0681743250")


#Creating the second tab
class Addresses(QWidget):
    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout(self)

        #Adding table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(30)
        self.tableWidget.setColumnCount(5)

        self.tableWidget.setItem(0,0, QTableWidgetItem("Name"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Mobile No."))
        self.tableWidget.setItem(0,2, QTableWidgetItem("Email"))
        self.tableWidget.setItem(0,3, QTableWidgetItem("Address"))
        self.tableWidget.setItem(0,4, QTableWidgetItem("Order No."))

        font = QFont()
        font.setBold(True)
        column=5
        for i in range(column):
            self.tableWidget.item(0, i).setFont(font)

        with open('orders.json') as f:
            data=json.load(f)
        row=2
        for orders in data['orders']:
            if orders['Name']=='Main':
                continue
            self.tableWidget.setItem(row,0, QTableWidgetItem(orders['Name']))
            self.tableWidget.setItem(row,1, QTableWidgetItem(orders['Mobile No.']))
            self.tableWidget.setItem(row,2, QTableWidgetItem(orders['Email']))
            self.tableWidget.setItem(row,3, QTableWidgetItem(orders['Address']))
            self.tableWidget.setItem(row,4, QTableWidgetItem(orders['Order No.']))
            row+=1

        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.mainLayout.addWidget(self.tableWidget)

        self.setLayout(self.mainLayout)
        
    @pyqtSlot(float, str)
    def add_table(self, average_km, route):
        groupBox = QGroupBox("Delivery list")
        vbox = QVBoxLayout()

        km_label = QLabel()
        km_label.setText("Average Distance to be travelled is {} Kilometres".format(average_km))
        km_label.setAlignment(Qt.AlignCenter)

        vbox.addWidget(km_label)

        tableWidget = QTableWidget()
        tableWidget.setRowCount(30)
        tableWidget.setColumnCount(5)
        tableWidget.setItem(0,0, QTableWidgetItem("Name"))
        tableWidget.setItem(0,1, QTableWidgetItem("Mobile No."))
        tableWidget.setItem(0,2, QTableWidgetItem("Email"))
        tableWidget.setItem(0,3, QTableWidgetItem("Address"))
        tableWidget.setItem(0,4, QTableWidgetItem("Order No."))

        font = QFont()
        font.setBold(True)
        column=5
        for i in range(column):
            tableWidget.item(0, i).setFont(font)

        row = 1
        with open('orders.json') as f:
            data=json.load(f)
        for i in route:
            for orders in data['orders']:
                if i=='0':
                    break
                if i==orders['S No.']:
                    tableWidget.setItem(row,0, QTableWidgetItem(orders['Name']))
                    tableWidget.setItem(row,1, QTableWidgetItem(orders['Mobile No.']))
                    tableWidget.setItem(row,2, QTableWidgetItem(orders['Email']))
                    tableWidget.setItem(row,3, QTableWidgetItem(orders['Address']))
                    tableWidget.setItem(row,4, QTableWidgetItem(orders['Order No.']))
                    break
            row += 1

        tableWidget.horizontalHeader().setStretchLastSection(True)
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        vbox.addWidget(tableWidget)
        groupBox.setLayout(vbox)

        self.mainLayout.addWidget(groupBox)



#Creating the third tab
class DeliveryGuys(QWidget):
    def __init__(self):
        super().__init__()

        #GroupBox 1: Delivery guys
        groupBox2 = QGroupBox("Delivery guys")
        vboxp = QVBoxLayout()

        self.guyR = QCheckBox("Raju")
        self.guyR.stateChanged.connect(lambda:self.checkbox(self.guyR))
        vboxp.addWidget(self.guyR)

        self.guyS = QCheckBox("Shaam")
        self.guyS.stateChanged.connect(lambda:self.checkbox(self.guyS))
        vboxp.addWidget(self.guyS)

        self.guyB = QCheckBox("Baburao")
        self.guyB.stateChanged.connect(lambda:self.checkbox(self.guyB))
        vboxp.addWidget(self.guyB)

        self.guyD = QCheckBox("Devi Prasad")
        self.guyD.stateChanged.connect(lambda:self.checkbox(self.guyD))
        vboxp.addWidget(self.guyD)

        self.button = QPushButton('Send', self)
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap("./icons and images/send_icon.png"))
        self.button.setIcon(self.icon)
        self.button.move(30, 30)
        self.button.clicked.connect(self.clickMethod)
        vboxp.addWidget(self.button)

        groupBox2.setLayout(vboxp)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(groupBox2)

        self.setLayout(self.mainLayout)

    def checkbox(self,b):
        if b.text() == "Raju":
           if b.isChecked() == True:
               name = "Raju"
               self.message(name)

        if b.text() == "Shaam":
           if b.isChecked() == True:
               name = "Shaam"
               self.message(name)

        if b.text() == "Baburao":
           if b.isChecked() == True:
               name = "Baburao"
               self.message(name)

        if b.text() == "Devi Prasad":
           if b.isChecked() == True:
               name = "Devi Prasad"
               self.message(name)

    def message(self, name):
        myfile = open('test.txt', 'r')
        list = myfile.read()

        message = "Mr {} following addresses are your today's target: \n\n".format(name)
        sno = 1
        with open('orders.json') as f:
            data=json.load(f)
        for i in list:
            for orders in data['orders']:
                if i == "0":
                    break
                if i == orders['S No.']:
                    message += "{}) {}, {}, {} \n".format(sno,orders['Name'],orders['Mobile No.'],orders['Address'])
                    message += "Tap on this for the location: "
                    message += "https://www.google.com/maps/place/{}+{}/@{},{},17z/data=!4m5!3m4!1s0x0:0x0!8m2!3d{}!4d{} \n\n".format(orders['Latitude'],orders['Longitude'],orders['Latitude'],orders['Longitude'],orders['Latitude'],orders['Longitude'])
                    sno += 1
                    break

        print(message)
        self.send_mail(message)

    def send_mail(self, message):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("aloyalways23@gmail.com", "Eminemrapgod")
        s.sendmail("aloyalways23@gmail.com", "aloyalways23@gmail.com", message)
        s.quit()

    def clickMethod(self):
        print("FUCK!!!")
        
    @pyqtSlot()
    def add_map(self):
        groupBox = QGroupBox("Delivery Map")
        vbox = QVBoxLayout()
        
        web = QWebEngineView()
        web.load(QUrl("file:///Users/aloy/Desktop/major/final_map.html"))
        web.show()
        
        vbox.addWidget(web)
        groupBox.setLayout(vbox)

        self.mainLayout.addWidget(groupBox)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
