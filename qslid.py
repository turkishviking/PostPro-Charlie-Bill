
from PyQt4.QtCore import SIGNAL
from PyQt4 import QtGui
class Qslid(QtGui.QSlider):

    def __init__(self, parent=None):
        QtGui.QSlider.__init__(self, parent)
        

    def resizeEvent(self, evt=None):
        self.emit(SIGNAL("resize()"))
        
