# -*- coding: utf-8 -*-

import os
import sys

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtOpenGL
from OpenGL import GLU
from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import array
from PyQt4 import QtCore, QtGui
from decimal import Decimal

class GLWidget(QtOpenGL.QGLWidget):

    def wheelEvent(self, event):
        super(GLWidget, self).wheelEvent(event)
        self.angle = self.angle +(event.delta()/12)
        self.resizeGL(self.w, self.h)
        self.updateGL()
        
    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == QtCore.Qt.LeftButton :
            self.mode = 1
            
    def mouseReleaseEvent(self, e):
        self.mode =0
        
    def mouseMoveEvent(self, event):
        if self.mode == 1:
            xx = event.pos().x()
            yy = event.pos().y()
            try:
                self.AngleX = self.AngleX + xx - self.xx1
                self.AngleY = self.AngleY + yy - self.yy1
            except (UnboundLocalError, NameError,  AttributeError):
                pass
           
            self.xx1 = xx
            self.yy1 = yy
            self.updateGL()
            
    
    def ajoute(self, li, listeCoo):
        self.listeMinMax = listeCoo
        self.liste = li
        
    
    def __init__(self, parent=None):
        self.angle = 70
        self.AngleX=0
        self.AngleY=0
        self.AngleZ=0
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.yRotDeg = 0.0
        self.setMouseTracking(True)
        self.mode = 0
        

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0,  0))
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, width, height):
        self.w = width
        self.h = height
        if height == 0: height = 1

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.aspect = width / float(height)
        #---------------------------------CAMERA-----------------------------------#
        GLU.gluPerspective(self.angle, self.aspect, 1.0, 1000.0)
        self.x = self.listeMinMax[3] + (self.listeMinMax[0]-self.listeMinMax[3] )/2
        self.y = self.listeMinMax[4] + (self.listeMinMax[1]-self.listeMinMax[4] )/2
        self.z = self.listeMinMax[5] + (self.listeMinMax[2]-self.listeMinMax[5] )/2
        xmax= (self.listeMinMax[0]-self.listeMinMax[3] )*Decimal(str(1.5))
        ymax= (self.listeMinMax[1]-self.listeMinMax[4] )*Decimal(str(1.5))
        zmax= (self.listeMinMax[2]-self.listeMinMax[5] )*Decimal(str(1.5))
      
        gluLookAt(xmax,ymax,zmax,self.x,self.y,self.z,0,0,1)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslated(self.x, self.y, self.z)
        glRotatef(self.AngleX/3, 1.0, 0.0, 0.0)
        glRotatef(self.AngleY/3, 0.0, 1.0, 0.0)
        glTranslated(-self.x, -self.y, -self.z)
        glPointSize (2.0)

        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw some stuff
        glBegin(GL_LINE_STRIP)
        for ligne in self.liste:
                x1 =ligne[0]
                y1 = ligne[1]
                z1 = ligne[2]
                glVertex3f(x1, y1, z1)

        glEnd()

    def initGeometry(self):
        self.cubeVtxArray = array(
                [[0.0, 0.0, 0.0],
                 [1.0, 0.0, 0.0],
                 [1.0, 1.0, 0.0],
                 [0.0, 1.0, 0.0],
                 [0.0, 0.0, 1.0],
                 [1.0, 0.0, 1.0],
                 [1.0, 1.0, 1.0],
                 [0.0, 1.0, 1.0]])
        self.cubeIdxArray = [
                0, 1, 2, 3,
                3, 2, 6, 7,
                1, 0, 4, 5,
                2, 1, 5, 6,
                0, 3, 7, 4,
                7, 6, 5, 4 ]
        self.cubeClrArray = [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [1.0, 0.0, 1.0],
                [1.0, 1.0, 1.0],
                [0.0, 1.0, 1.0 ]]





class MonDialog(object):
    
    def setupUi(self, Dialog, datas, listeCoo,  sender):
        self.datas, self.sender = datas,  sender
        self.listeCoo,  self.sender = listeCoo,  sender
    
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(800, 600)
        self.gl = GLWidget(Dialog)
        self.gl.resize(800, 600)
        self.gl.ajoute(self.datas, self.listeCoo)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)


        self.horizontalLayout.addWidget(self.gl)

        self.gl.setSizePolicy(sizePolicy)

