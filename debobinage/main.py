#! /usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
from PyQt4 import QtGui
from form import Form


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("debo")

    myapp = Form()
    myapp.show()
    sys.exit(app.exec_())
