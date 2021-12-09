# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 15:21:44 2021

@author: ShendR
"""

from SPI_GUI_black_6 import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QDialog

import spi_data_class_black_5
import monitor_file_handling_gui_2

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import numpy as np


class SPI_GUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
            # Canvas on GUI       
        self.Big_graphicsView = Canvas(parent=self.centralwidget)
        self.Big_graphicsView.setMinimumSize(QtCore.QSize(500, 400))
        self.Big_graphicsView.setObjectName("Big_graphicsView")
        self.Big_graphicsView.setStyleSheet("background-color: rgb(58, 59, 61);\n"
"border-color: rgb(0, 0, 0);")
        self.gridLayout.addWidget(self.Big_graphicsView, 2, 0, 1, 1)
        
            # Toolbar on GUI
        self.toolbar = NavigationToolbar(self.Big_graphicsView, self.Big_graphicsView) 
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        
            # SPI data Class
        self.spi_tdms = spi_data_class_black_5.SPI_tDMS_Data()
            # Open file with GUI - button or Ctrl+O
        self.menuFile.triggered.connect((lambda: self.open_file()))
        self.actionOpen_TDMS_file.setShortcut('Ctrl+O')
        
            # Set up Advanced Tab
        self.advanced_tab()
        self.read_data_zs = monitor_file_handling_gui_2
        
            # Set up TextBox - for adding text messages
        self.setup_logbook()
            
            # Button cliked - select channel from list
        self.ParamterPlot_button.clicked.connect(lambda: self.plot_button(self.Big_graphicsView, from_t=self.from_time1.text(), to_t=self.to_time1.text(), channel=self.selected_item))
        self.from_time1.returnPressed.connect(lambda: self.plot_button(self.Big_graphicsView, from_t=self.from_time1.text(), to_t=self.to_time1.text(), channel=self.selected_item))
        self.to_time1.returnPressed.connect(lambda: self.plot_button(self.Big_graphicsView, from_t=self.from_time1.text(), to_t=self.to_time1.text(), channel=self.selected_item))
        self.filtered_button.clicked.connect(lambda: self.filtered_list())
        self.allchannels_button.clicked.connect(lambda: self.show_all_list())
        
        self.plot_multi_button.clicked.connect(lambda: self.multi_plot_button(self.Big_graphicsView, from_t=self.from_time2.text(), to_t=self.to_time2.text(), multi_channels=self.x))
        self.from_time2.returnPressed.connect(lambda: self.multi_plot_button(self.Big_graphicsView, from_t=self.from_time2.text(), to_t=self.to_time2.text(), multi_channels=self.x))
        self.to_time2.returnPressed.connect(lambda: self.multi_plot_button(self.Big_graphicsView, from_t=self.from_time2.text(), to_t=self.to_time2.text(), multi_channels=self.x))
        
        self.overplot_button.clicked.connect(lambda: self.overplot_button1(self.Big_graphicsView, from_t=self.from_time2.text(), to_t=self.to_time2.text(), multi_channels=self.x))
        self.diff_button.clicked.connect(lambda: self.diff_button_func(self.Big_graphicsView, from_t=self.from_time2.text(), to_t=self.to_time2.text(), multi_channels=self.x))
        
        self.plot_multi_button_2.clicked.connect(lambda: self.plot_zs_data(self.Big_graphicsView,
                                                                           data_names=self.x2,
                                                                           startdate=self.startdate.text(),
                                                                           starttime=self.starttime.text(),
                                                                           start_datetime=self.start_datetime.text(),
                                                                           enddate=self.enddate.text(),
                                                                           endtime=self.endtime.text(),
                                                                           end_datetime=self.end_datetime.text()))
        self.starttime.returnPressed.connect(lambda: self.plot_zs_data(self.Big_graphicsView,
                                                                           data_names=self.x2,
                                                                           startdate=self.startdate.text(),
                                                                           starttime=self.starttime.text(),
                                                                           start_datetime=self.start_datetime.text(),
                                                                           enddate=self.enddate.text(),
                                                                           endtime=self.endtime.text(),
                                                                           end_datetime=self.end_datetime.text()))
        self.endtime.returnPressed.connect(lambda: self.plot_zs_data(self.Big_graphicsView,
                                                                           data_names=self.x2,
                                                                           startdate=self.startdate.text(),
                                                                           starttime=self.starttime.text(),
                                                                           start_datetime=self.start_datetime.text(),
                                                                           enddate=self.enddate.text(),
                                                                           endtime=self.endtime.text(),
                                                                           end_datetime=self.end_datetime.text()))




        # After a file is opened - update GUI        
    def open_file(self):          
        self.Parameter_listView.clear()
        self.Parameter_listView_2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.Parameter_listView.setAlternatingRowColors(False)
        self.Parameter_listView_2.clear()
        self.Parameter_listView_2.setAlternatingRowColors(False)
        self.ShotID_box.clear()
        self.spi_tdms = spi_data_class_black_5.SPI_tDMS_Data()
        self.spi_tdms.run_open_tdms()
        shot_id = self.spi_tdms.root_obj_values[0]
        self.ShotID_box.setText(shot_id)
        channels = self.spi_tdms.channels
        for i in channels:
            self.Parameter_listView.addItem(str(i))
            self.Parameter_listView_2.addItem(str(i))
        self.Parameter_listView.itemClicked.connect(self.listitemclicked)
        self.Parameter_listView_2.itemClicked.connect(self.listitemsclicked)
        
        
        
        # Button cliked - select single channel from list
    def listitemclicked(self):
        self.selected_item = self.Parameter_listView.currentItem().text()
        self.logbook.append('Item in the list is clicked:  ' + self.selected_item)
        return self.selected_item
    
    
    
        # Select multiple channels from list - max. 6 channels
    def listitemsclicked(self):
        self.selected_items = self.Parameter_listView_2.currentItem().text()
        items = self.Parameter_listView_2.selectedItems()
        self.x = []
        for i in range(len(items)):
            self.x.append(str(self.Parameter_listView_2.selectedItems()[i].text()))
            if len(self.x) > 6:
                self.x.pop(0)                
        print(self.x)
        self.logbook.append('Item is added to selection:  ' + self.selected_items)
        return self.x
    
    
    def adv_listitemsclicked(self):
#        self.selected_items = self.Parameter_listView_3.currentItem().text()
#        items = self.Parameter_listView_3.selectedItems()
#        self.x2 = []
#        for i in range(len(items)):
#            self.x2.append(str(self.Parameter_listView_3.selectedItems()[i].text()))
#            if len(self.x2) > 6:
#                self.x2.pop(0)                
#        print(self.x2)
#        self.logbook.append('Item is added to selection:  ' + self.selected_items)
#        return self.x2
        self.x2 = self.Parameter_listView_3.currentItem().text()
        self.logbook.append('Item in the list is clicked:  ' + self.x2)
        return self.x2
    
    
    
        # Set up TextBox - for adding messages
    def setup_logbook(self, text='check'):
        self.logbook = self.Big_textBrowser
        font = self.logbook.font()
        font.setFamily("Courier")
        font.setPointSize(8)        
        self.logbook.append("Welcome to SPI sensor data: Open tDMS file")
        self.logbook.moveCursor(QtGui.QTextCursor.End)
        self.logbook.ensureCursorVisible()
        
        
        
        # When Plot Single Channel Button is pushed - running this method
    def plot_button(self, canvas, from_t, to_t, channel):
        try:
            self.logbook.append('Plotting selected item: ' + channel)
            if from_t == "None":
                from_t = None
            else:
                from_t = int(from_t)
            if to_t == "None":
                to_t = None
            else:
                to_t = int(to_t)    
                
            self.spi_tdms.plot_one_channel(canvas, from_t, to_t, channel)
            
            interval_data = np.array(self.spi_tdms.get_data_interval(from_t, to_t, channel)[0])
            self.max_lineEdit.setText(str(round(interval_data.max(),3)))
            self.min_lineEdit.setText(str(round(interval_data.min(),3)))
            self.mean_lineEdit.setText(str(round(interval_data.mean(),3)))
                       
        except:
            self.logbook.append("<span style=\"color:#ff0000\" >"+'Error plotting request'+"</span>")
            
            
                
         # When Plot Multiple Channel Button is pushed - running this method        
    def multi_plot_button(self, canvas, from_t, to_t, multi_channels):
        try:
            no_of_channels = len(multi_channels)
            print("Number of channels selected: " + str(no_of_channels))
            self.logbook.append("Number of channels selected: " + str(no_of_channels))
            if from_t == "None":
                from_t = None
            else:
                from_t = int(from_t)
            if to_t == "None":
                to_t = None
            else:
                to_t = int(to_t)   
            self.spi_tdms.plot_multi_ch(canvas, from_t, to_t, multi_channels)
        except:
            self.logbook.append("<span style=\"color:#ff0000\" >"+'Error plotting request'+"</span>")

                
                
    def overplot_button1(self, canvas, from_t, to_t, multi_channels):
        try:
            no_of_channels = len(multi_channels)
            print("Number of channels selected: " + str(no_of_channels))
            self.logbook.append("Number of channels selected: " + str(no_of_channels))
            if from_t == "None":
                from_t = None
            else:
                from_t = int(from_t)
            if to_t == "None":
                to_t = None
            else:
                to_t = int(to_t)   
            self.spi_tdms.overplot_multi_ch(canvas, from_t, to_t, multi_channels)
        except:
            self.logbook.append("<span style=\"color:#ff0000\" >"+'Error plotting request'+"</span>")
 
                
                
    def diff_button_func(self, canvas, from_t, to_t, multi_channels):
        try:
            no_of_channels = len(multi_channels)
            print("Number of channels selected: " + str(no_of_channels))
            self.logbook.append("Number of channels selected: " + str(no_of_channels))
            if from_t == "None":
                from_t = None
            else:
                from_t = int(from_t)
            if to_t == "None":
                to_t = None
            else:
                to_t = int(to_t)   
            self.spi_tdms.diff_plot(canvas, from_t, to_t, multi_channels)
        except:
            self.logbook.append("<span style=\"color:#ff0000\" >"+'Error plotting request'+"</span>")
                

                
    def filtered_list(self):
        filtered_list = ['Cryo Press 0 (PM1)', 
                         'Cryo Press 1 (PM2)',
                         'Cryo Press 2 (PM3)',
                         'Cryo Press 3 (PM4)',
                         'Cryo Press 4 (PM5)',
                         'T1 - Barrel Temp',
                         'T2 - CHead Bottom',
                         'T3 - CHead Top',
                         'T4 - He Connection',
                         'T5 - He Distributor',
                         'T6 - Heat Shield',
                         'T7 - HeatExc DownStr ',
                         'T8 - HeatExc UpStr']
        
        self.Parameter_listView.clear()
        self.Parameter_listView_2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.Parameter_listView.setAlternatingRowColors(False)
        self.Parameter_listView_2.clear()
        self.Parameter_listView_2.setAlternatingRowColors(False)
        for i in filtered_list:
            self.Parameter_listView.addItem(str(i))
            self.Parameter_listView_2.addItem(str(i))
        self.Parameter_listView.itemClicked.connect(self.listitemclicked)
        self.Parameter_listView_2.itemClicked.connect(self.listitemsclicked)
        
        
    def show_all_list(self):
        self.Parameter_listView.clear()
        self.Parameter_listView_2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.Parameter_listView.setAlternatingRowColors(False)
        self.Parameter_listView_2.clear()
        self.Parameter_listView_2.setAlternatingRowColors(False)
        channels = self.spi_tdms.channels
        for i in channels:
            self.Parameter_listView.addItem(str(i))
            self.Parameter_listView_2.addItem(str(i))
        self.Parameter_listView.itemClicked.connect(self.listitemclicked)
        self.Parameter_listView_2.itemClicked.connect(self.listitemsclicked)
        
        
        
    def advanced_tab(self):
        filtered_list = ['Cryo Press 0 (PM1)', 
                         'Cryo Press 1 (PM2)',
                         'Cryo Press 2 (PM3)',
                         'Cryo Press 3 (PM4)',
                         'Cryo Press 4 (PM5)',
                         'T1 - Barrel Temp',
                         'T2 - CHead Bottom',
                         'T3 - CHead Top',
                         'T4 - He Connection',
                         'T5 - He Distributor',
                         'T6 - Heat Shield',
                         'T7 - HeatExc DownStr ',
                         'T8 - HeatExc UpStr']
        
#        self.Parameter_listView.clear()
#        self.Parameter_listView_3.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
#        self.Parameter_listView.setAlternatingRowColors(False)
        self.Parameter_listView_3.clear()
        self.Parameter_listView_3.setAlternatingRowColors(False)
        for i in filtered_list:
            self.Parameter_listView_3.addItem(str(i))
#        self.Parameter_listView.itemClicked.connect(self.listitemclicked)
        self.Parameter_listView_3.itemClicked.connect(self.adv_listitemsclicked)
        self.ShotID_box.setText('Shot_ID')

                
        
    def plot_zs_data(self,canvas,data_names,startdate,starttime,start_datetime,
                     enddate,endtime,end_datetime):
        try:            
            no_of_channels = len(data_names)
            print("Number of channels selected: " + str(no_of_channels))
            self.logbook.append("Number of channels selected: " + str(no_of_channels))
            self.logbook.append("Plotting in progress")
            if startdate == "None":
                startdate = None
            else:
                startdate = startdate
            if starttime == "None":
                starttime = None
            else:
                starttime = starttime
            if start_datetime == "None":
                start_datetime = None
            else:
                start_datetime = start_datetime
            if enddate == "None":
                enddate = None
            else:
                enddate = enddate
            if endtime == "None":
                endtime = None
            else:
                endtime = endtime
            if end_datetime == "None":
                end_datetime = None
            else:
                end_datetime = end_datetime

            read_data = self.read_data_zs.read_data(data_names, startdate, starttime, start_datetime,
                                                     enddate, endtime, end_datetime)
                        
            x_data = read_data[0]
            y_data = read_data[1][0]
            canvas.fig.clf()
            axes = canvas.fig.add_subplot(111)
            axes.plot(x_data, y_data)
            axes.set_facecolor('None')
            axes.set_ylabel(data_names[0] + ' ' + '[' + read_data[2][0] + ']')    
            axes.set_xlabel('Time' +' [yyyy-MM-dd HH:mm:ss]')
            axes.spines['bottom'].set_color('white')
            axes.spines['top'].set_color('white') 
            axes.spines['right'].set_color('white')
            axes.spines['left'].set_color('white')
            axes.xaxis.label.set_color('white')
            axes.yaxis.label.set_color('white')
            axes.tick_params(colors='white', which='both')           
            canvas.draw()
            
            
#            dict1 = {}
#            channels_data = data_names
#            x_data = read_data[0]
#            count=1
#            for i in channels_data:
#                if i != None:
#                    dict1[i] = read_data[count]
#                    count+=1
#                else:
#                    break
#                    
#            channels_no = 0
#            for j in channels_data:
#                if j != None:
#                    channels_no+=1
#            
#            canvas.fig.clf()
#            axes = canvas.fig.subplots(1,1)   
#            part1 = axes.twinx()
#            
#            for i in range(channels_no):
#                if dict1[channels_data[0]][1] == dict1[channels_data[i]][1]:
#                    axes.plot(x_data[0], dict1[channels_data[i]][0], label=channels_data[i])
#                    axes.set_ylabel(channels_data[i] + " [" + dict1[channels_data[i]][1] + "]")
#                    axes.set_facecolor('None')
#                    axes.spines['bottom'].set_color('white')
#                    axes.spines['top'].set_color('white') 
#                    axes.spines['right'].set_color('white')
#                    axes.spines['left'].set_color('white')
#                    axes.tick_params(colors='white', which='both')           
#                    legend = axes.legend(loc='upper left')
#                    legend.get_frame().set_facecolor('None')
#                    for text in legend.get_texts():
#                        text.set_color("white")
#                else:
#                    part1.plot(x_data[0], dict1[channels_data[i]][0], label=channels_data[i])
#                    part1.set_ylabel(channels_data[i] + " [" + dict1[channels_data[i]][1] + "]")
#                    part1.set_facecolor('None')
#                    part1.spines['bottom'].set_color('white')
#                    part1.spines['top'].set_color('white') 
#                    part1.spines['right'].set_color('white')
#                    part1.spines['left'].set_color('white')
#                    part1.tick_params(colors='white', which='both')           
#                    legend = part1.legend(loc='upper right')
#                    legend.get_frame().set_facecolor('None')
#                    for text in legend.get_texts():
#                        text.set_color("white")
#                axes.set_xlabel('TimeStamp [s]')  
            
            
            self.logbook.append("DONE")
            
        except:
            self.logbook.append("<span style=\"color:#ff0000\" >"+'Error plotting request'+"</span>")
            
                
                

    # Canvas on GUI to plot on
class Canvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure()
        self.fig.clear()
        self.fig.patch.set_facecolor('None')
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('None')
        self.axes.axis('off')
        super(Canvas, self).__init__(self.fig)      
        
       
         
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    
    widget = SPI_GUI()
    widget.show()
    
    app.exec_()