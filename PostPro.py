#! /usr/bin/python
#-*- coding: utf-8 -*-
from PyQt4 import QtGui
from Form1 import MainWindow
import sys
import os

if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   app.setApplicationName("PostPro--Charlybill")
   myapp = MainWindow()
   myapp.show()
   sys.exit(app.exec_())
   
