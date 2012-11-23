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
    global liste
    global listeMinMax
    global mode
    global xx1
    global yy1
    global AngleX
    global AngleY
    global AngleZ
    global angle
    
    def wheelEvent(self, event):
        super(GLWidget, self).wheelEvent(event)
        global angle
        global h
        global w
        angle = angle +(event.delta()/12)
        self.resizeGL(w, h)
        self.updateGL()
        
    def mousePressEvent(self, mouseEvent):
        global mode
        if mouseEvent.button() == QtCore.Qt.LeftButton :
            mode = 1
            
    def mouseReleaseEvent(self, e):
        global mode
        mode =0
        
  
    def mouseMoveEvent(self, event):
        global xx1
        global yy1
        global mode
        global AngleX
        global AngleY
        global AngleZ
        if mode == 1:
            xx = event.pos().x()
            yy = event.pos().y()
            try:
                AngleX = AngleX + xx - xx1
                AngleY = AngleY + yy - yy1
            except (UnboundLocalError, NameError):
                pass
           
            xx1 = xx
            yy1 = yy
            self.updateGL()
            
    
    def ajoute(self, li, listeCoo):
        global liste
        global listeMinMax 
        listeMinMax = listeCoo
        liste = li
        
    
    def __init__(self, parent=None):
        global mode
        global AngleX
        global AngleY
        global AngleZ
        global angle
        angle = 70
        AngleX=0
        AngleY=0
        AngleZ=0
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.yRotDeg = 0.0
        self.setMouseTracking(True)
        mode = 0
        

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0,  0))
  
        
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, width, height):
        global listeMinMax
        global x
        global y
        global z
        global aspect
        global angle
        global w
        global h

        w = width
        h = height
        if height == 0: height = 1

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)
        #---------------------------------CAMERA-----------------------------------#
        GLU.gluPerspective(angle, aspect, 1.0, 1000.0)
        
        x = listeMinMax[3] + (listeMinMax[0]-listeMinMax[3] )/2
        y = listeMinMax[4] + (listeMinMax[1]-listeMinMax[4] )/2
        z = listeMinMax[5] + (listeMinMax[2]-listeMinMax[5] )/2
        xmax= (listeMinMax[0]-listeMinMax[3] )*Decimal(1.5)
        ymax= (listeMinMax[1]-listeMinMax[4] )*Decimal(1.5)
        zmax= (listeMinMax[2]-listeMinMax[5] )*Decimal(1.5)
      
        print ((listeMinMax))
        print(x, y, z)
        gluLookAt(xmax,ymax,zmax,x,y,z,0,0,1)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        global liste
        global x
        global y
        global z
        global AngleX
        global AngleY
        global AngleZ
        global angle
        global aspect
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
       

        glLoadIdentity()
        

        glTranslated(x, y, z)
        glRotatef(AngleX/3, 1.0, 0.0, 0.0)
        glRotatef(AngleY/3, 0.0, 1.0, 0.0)
        glTranslated(-x, -y, -z)
        glPointSize (2.0)

    
        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw some stuff
        glBegin(GL_LINE_STRIP)
        for ligne in liste:
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







        
