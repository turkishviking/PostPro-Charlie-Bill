# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/in-triz/PostPro-Charlie-Bill/test.ui'
#
# Created: Wed Nov 28 18:57:26 2012
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form, liste):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(901, 644)
        self.textEdit = QtGui.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(20, 20, 861, 591))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        for d in liste:
            self.textEdit.append(d)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

