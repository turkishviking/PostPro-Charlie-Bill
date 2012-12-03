 -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature

from Ui_APropo import Ui_Dialog

class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
    
    @pyqtSignature("QString")
    def on_label_linkActivated(self, link):
        """
        Slot documentation goes here.
        """
        QDesktopServices.openUrl(QUrl("http://www.google.fr/"))
