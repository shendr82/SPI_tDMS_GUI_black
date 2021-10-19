# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 15:21:44 2021

@author: ShendR
"""

from SPI_GUI3c import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QDialog

import spi_class_new3

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


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
        self.spi_tdms = spi_class_new3.SPI_tDMS_Data()
            # Open file with GUI - button or Ctrl+O
        self.menuFile.triggered.connect((lambda: self.open_file()))
        self.actionOpen_TDMS_file.setShortcut('Ctrl+O')
        
            # Set up TextBox - for adding text messages
        self.setup_logbook()
            
            # Button cliked - select channel from list
#        self.ParamterPlot_button.clicked.connect(lambda: self.plot_button(self.Big_graphicsView, self.from_time1.text(), self.to_time1.text(), channel=self.selected_item))
        self.ParamterPlot_button.clicked.connect(lambda: self.plot_button(self.Big_graphicsView, from_t=self.from_time1.text(), to_t=self.to_time1.text(), channel=self.selected_item))
        self.plot_multi_button.clicked.connect(lambda: self.multi_plot_button(self.Big_graphicsView, from_t=self.from_time2.text(), to_t=self.to_time2.text(), multi_channels=self.x))


        # After a file is opened - update GUI        
    def open_file(self):  
        self.spi_tdms.run_open_tdms()
        shot_id = self.spi_tdms.root_obj_values[0]
        self.ShotID_box.setText(shot_id)
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
    
    
    
        # Set up TextBox - for adding messages
    def setup_logbook(self, text='check'):
        self.logbook = self.Big_textBrowser
        font = self.logbook.font()
        font.setFamily("Courier")
        font.setPointSize(8)        
        self.logbook.append("Welcome to SPI sensor data: Open tDMS file")
        self.logbook.moveCursor(QtGui.QTextCursor.End)
#        self.logbook.setStyleSheet("color: white; background-color: rbg(58, 59, 61);")
        self.logbook.ensureCursorVisible()
        
        
        # When Plot Button is pushed - running this method
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
        except:
            self.logbook.append("<span style=\"color:#ff0000\" >"+'Error plotting request'+"</span>")
            
            
    def multi_plot_button(self, canvas, from_t, to_t, multi_channels):
        try:
            no_of_channels = len(multi_channels)
            print("Number of channels selected: " + str(no_of_channels))
            self.logbook.append("Multiple channels are selected: No. of channels " + str(no_of_channels))
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