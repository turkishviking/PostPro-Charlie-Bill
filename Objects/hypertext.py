from PyQt4.QtCore import SIGNAL,  QUrl
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtGui import  QDesktopServices
class Hypertext(QtGui.QLabel):

    def __init__(self, parent=None):
        QtGui.QSlider.__init__(self, parent)
        self.setCursor(QtCore.Qt.PointingHandCursor)
    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == QtCore.Qt.LeftButton :
            QDesktopServices.openUrl(QUrl("http://www.in-triz.com/"))
 
