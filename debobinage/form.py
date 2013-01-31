# -*- coding: utf-8 -*-

"""
Module implementing Form.
"""

from PyQt4.QtGui import QWidget,  QApplication,  QKeyEvent
from PyQt4.QtCore import pyqtSignature,  Qt


from Ui_form import Ui_Form

class Form(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QWidget.__init__(self, parent)
        self.setupUi(self)
    
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        
        
        """
        self.go()
        
    def go(self):
        try:
            x = float(self.lineEdit.text())
            z = x
            y = x % 360
            self.pressPaper = QApplication.clipboard()
            if y < 180:
                self.lineEdit_2.setText("G0 C-" + str(y))
                self.pressPaper.setText("G0 C-" + str(y))
            else:
                self.lineEdit_2.setText("G0 C+" + str(360 - y))
                y = 360 - y
                self.pressPaper.setText("G0 C+" + str(y))
        except:
            pass
            
    def keyPressEvent(self, event):
        if type(event) == QKeyEvent and event.key() == Qt.Key_Enter : 
            self.go()

        
