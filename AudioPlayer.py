# -*- coding: utf-8 -*-

import sys, os
from PyQt4 import QtCore, QtGui, uic
from PyQt4.phonon import Phonon
from PyQt4.QtCore import QCoreApplication


class AudioPlayer(QtGui.QWidget):
    def __init__(self, parent = None):
        
        self.url = "http://listen.radionomy.com/dubsideradio"

        QtGui.QWidget.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Preferred)


        self.player = Phonon.createPlayer(Phonon.MusicCategory,
            Phonon.MediaSource(self.url))
        self.player.setTickInterval(100)
        self.player.tick.connect(self.tock)

        self.play_pause = QtGui.QPushButton(self)
        
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(("image/play.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_pause.setIcon(self.icon)
        self.play_pause.setIconSize(QtCore.QSize(23, 24))
        self.icon2 = QtGui.QIcon()
        self.icon2.addPixmap(QtGui.QPixmap(("image/pause.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_pause.setFlat(True)
        self.play_pause.clicked.connect(self.playClicked)
        self.player.stateChanged.connect(self.stateChanged)

        self.slider = Phonon.SeekSlider(self.player , self)
        self.setWindowIcon(self.icon)
        self.status = QtGui.QLabel(self)
        self.status.setAlignment(QtCore.Qt.AlignRight |
            QtCore.Qt.AlignVCenter)
        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(self.play_pause)
        layout.addWidget(self.slider)
        layout.addWidget(self.status)


    def playClicked(self):
        if self.player.state() == Phonon.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def stateChanged(self, new, old):
        if new == Phonon.PlayingState:
            self.play_pause.setIcon(self.icon2)
      
        else:
            self.play_pause.setIcon(self.icon)

    def tock(self, time):
        time = time/1000
        h = time/3600
        m = (time-3600*h) / 60
        s = (time-3600*h-m*60)
        self.status.setText('%02d:%02d:%02d'%(h,m,s))
        
    def closeEvent(self, e):
        self.player.stop()

