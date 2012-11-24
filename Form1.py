# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QFileDialog
from Ui_Form1 import Ui_MainWindow
import math
from decimal import Decimal

import os
from PyQt4 import QtCore, QtGui
import OGL

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.unit = "G21"
        self.deplacement = "G90"
        self.PlandeTravail = "G17"
        self.coordonnees = "G54"
        self.connect(self.verticalSlider, QtCore.SIGNAL("resize()"), self.resizedW)

        
    def resizedW(self):
        self.NbrLigneAffiche = int(self.InputTextEdit.height()/13.5)
        try:
            self.TransformTextEdit.clear()
            for g in range(self.verticalSlider_2.value(), self.verticalSlider_2.value()+ self.NbrLigneAffiche):
                self.listeCalcul [g] = str(self.listeCalcul [g]).replace("\r\n", "")
                self.TransformTextEdit.append(self.listeCalcul [g])
        except AttributeError:
            pass
            
        try:
            self.InputTextEdit.clear()
            for g in range(self.verticalSlider.value(), self.verticalSlider.value()+ self.NbrLigneAffiche):
                self.liste[g] = self.liste[g].replace("\r\n", "")
                self.InputTextEdit.append(self.liste[g])
        except AttributeError:
            pass
        print(self.NbrLigneAffiche)
    @pyqtSignature("")
    def on_BouttonEffacer_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
        
    @pyqtSignature("")
    def on_BoutonPrevusalisation_clicked(self):
        """
        Slot documentation goes here.
        """
        Dialog = QtGui.QDialog()
        di = OGL.MonDialog()
        di.setupUi(Dialog, self.liste3D, self.listeCoo,  self)
        reply = Dialog.exec_()

    
    """-----------------------------------------------------------------------------------------\\\\\\\\\\----------Calcul-----------////////----------------------------------------------------------------------------"""
    @pyqtSignature("")
    def on_BouttonCalcul_clicked(self):
        """
        Slot documentation goes here.
        """
        self.liste3D = []
        self.Stock_C = 0
        self.listeCalcul = []
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(len(self.liste))
        Bol_Calcul = False
        #-------------------------------------Vitesse Rapide pour Simulation--------------------------------------#
        if self.checkBox.isChecked() == True:
            self.listeHeader.append("G1 " + "F10000000000")
        #---------------------------------\\\\\\------Traitement des données------///////------------------------------#
        #-----------------------------------------------------Prend l'outil----------------------------------------------------#
        
        for ligne in self.liste:
            self.progressBar.setValue( self.progressBar.value()+1)
            if "LOADTL/" in ligne:
                self.listeCalcul .append("M5")
                self.listeCalcul .append("T" + ligne.replace("LOADTL/", "") + " G43")
                self.listeCalcul .append("M6")
                self.listeCalcul .append("M3")
                self.listeCalcul .append("M0")
                
            if self.checkBox.isChecked() == False:
                if "FEDRAT/ " in ligne:
                    ligne=ligne.replace("FEDRAT/ ", "")
                    ligne=ligne.replace(",MMPM", "")
                    self.listeCalcul .append("G1 F" + (ligne))
                    
            #----------------------------------------------------Extraction-----------------------------------------------------#
            if "GOTO" in ligne:
                self.listeCalcul .append(self.Extraction(ligne,  Bol_Calcul))
                Bol_Calcul = True

        #---------------------------------Affiche les 28 premier élement de la liste-----------------------------#
        self.verticalSlider_2.setMaximum(len(self.listeCalcul ))
        try:
            for g in range(28):
                self.listeCalcul [g]=str(self.listeCalcul [g]).replace("\r\n", "")
                self.progressBar.setValue(self.progressBar.value()+1)
                self.TransformTextEdit.append(self.listeCalcul [g])
        except (NameError,  IndexError):
            pass
            
    """--------------------------------------------------------------------------------------Header, Ender------------------------------------------------------------------------------------------------------"""

    #-------------------------------------------------------Header-----------------------------------------------------#
    def Header(self):
        self.HeadertextEdit.clear()
        self.HeadertextEdit.append("%")
        self.HeadertextEdit.append(self.unit)
        self.HeadertextEdit.append(self.deplacement)
        self.HeadertextEdit.append(self.PlandeTravail)
        self.HeadertextEdit.append(self.coordonnees)

    #-------------------------------------------------------Ender-----------------------------------------------------#
    def Ender(self):
        self.EnderTextEdit.clear()
        self.EnderTextEdit.append("M05")
        self.EnderTextEdit.append("M2")
        self.EnderTextEdit.append("%")


    """-----------------------------------------------------------------------------------------------Paramètres Machines-------------------------------------------------------------------------------"""
    
    @pyqtSignature("QString")
    def on_comboBoxUnite_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        """
        if str(p0) == "mm":
            self.unit = "G21"
        else:
            self.unit = "G20"
        self.Header()
    
    @pyqtSignature("QString")
    def on_comboBoxType_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        """
       
        if str(p0) == "Absolues":
            self.deplacement = "G90"
        else:
            self.deplacement = "G91"
        self.Header()
    
    @pyqtSignature("QString")
    def on_comboBoxPlan_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        """

        if str(p0) == "XY":
            self.PlandeTravail = "G17"
        elif str(p0) == "XZ":
            self.PlandeTravail = "G18"
        else:
            self.PlandeTravail = "G19"
        self.Header()
    
    @pyqtSignature("QString")
    def on_comboBoxCoordonees_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        """
        
        if str(p0) == "Origine piece 1":
            self.coordonnees = "G54"
        if str(p0) == "Origine piece 2":
            self.coordonnees = "G55"
        if str(p0) == "Origine piece 3":
            self.coordonnees = "G56"
        if str(p0) == "Origine piece 4":
            self.coordonnees = "G57"
        if str(p0) == "Origine piece 5":
            self.coordonnees = "G58"
        if str(p0) == "Origine piece 6":
            self.coordonnees = "G59"
        if str(p0) == "Origine piece 7":
            self.coordonnees = "G59.1"
        if str(p0) == "Origine piece 8":
            self.coordonnees = "G59.2"
        if str(p0) == "Origine piece 9":
            self.coordonnees = "G59.3"
        self.Header()
        
    """--------------------------------------------------------------------------------------------------Gestion des slider------------------------------------------------------------------------------------------"""
    @pyqtSignature("int")
    def on_verticalSlider_valueChanged(self, value):
        """
        Slot documentation goes here.
        """
        try:
            self.InputTextEdit.clear()
            for g in range(self.verticalSlider.value(), self.verticalSlider.value()+ self.NbrLigneAffiche):
                self.liste[g] = self.liste[g].replace("\r\n", "")
                self.InputTextEdit.append(self.liste[g])
            self.spinBox.setMaximum(len(self.liste))
            self.spinBox.setValue(self.verticalSlider.value())
        except (NameError,  IndexError,  AttributeError):
            pass
            
    @pyqtSignature("int")
    def on_verticalSlider_2_valueChanged(self, value):
        """
        Slot documentation goes here.
        """

        try:
            self.TransformTextEdit.clear()
            for g in range(self.verticalSlider_2.value(), self.verticalSlider_2.value()+ self.NbrLigneAffiche):
                self.listeCalcul [g] = str(self.listeCalcul [g]).replace("\r\n", "")
                self.TransformTextEdit.append(self.listeCalcul [g])
            self.spinBox_2.setMaximum(len(self.listeCalcul ))
            self.spinBox_2.setValue(self.verticalSlider_2.value())
        except (NameError,  IndexError,  AttributeError):
            pass
    """---------------------------------------------------------------------------------------------------Gestion des spinBox-------------------------------------------------------------------------------------------"""
    @pyqtSignature("int")
    def on_spinBox_valueChanged(self, p0):
        """
        Slot documentation goes here.
        """
        self.verticalSlider.setValue(self.spinBox.value())
      
    
    @pyqtSignature("int")
    def on_spinBox_2_valueChanged(self, p0):
        """
        Slot documentation goes here.
        """
        self.verticalSlider_2.setValue(self.spinBox_2.value())
        
    """--------------------------------------------------------------------------------------------------Gestion des Menus------------------------------------------------------------------------------------------"""
        
    @pyqtSignature("int")
    def on_menuA_propos_activated(self, itemId):
        """
        Slot documentation goes here.
        """

    
    @pyqtSignature("int")
    def on_menuAide_activated(self, itemId):
        """
        Slot documentation goes here.
        """

    
    
    """--------------------------------------------------------------------------------------------------Ouvrir un fichier et prévisualiser-----------------------------------------------------------------------------------------"""
    @pyqtSignature("")
    def  on_actionOuvrir_et_pr_visualiser_activated(self):
        """
        Slot documentation goes here.
        """
        try:
            #--------------------------------Selection du Fichier, ouverture en lecture-----------------------------#
            filename=QFileDialog.getOpenFileName(self, "Explorateur de Fichier – Ouvrir un Fichier", "", "AptSource (*.aptsource)")
            fichier = open(filename, "r")
            self.Header()
            self.Ender()
            #----------------------------------Met la collection d ligne dans une liste--------------------------------#
            self.liste = fichier.readlines()
            self.progressBar.setMaximum(len(self.liste))
            #----------------------------------Extrait les coordonnées pour openGL--------------------------------#
            self.liste3D=[]
            self.listeCoo=[]
            
            for ligne in self.liste:
                self.progressBar.setValue(self.progressBar.value()+1)
                if "GOTO" in ligne:
                    ligne = ligne.replace("GOTO", "")
                    ligne = ligne.replace("/", "")
                    self.listeValeur = ligne.split(",")
                    X = Decimal(self.listeValeur[0])
                    Y = Decimal(self.listeValeur[1])
                    Z = Decimal(self.listeValeur[2])
                    #-------------Extrait les coordonnée max pour le placement de la caméra---------#
                    try:
                        if Xmax < X: Xmax = X
                        if Ymax < Y: Ymax = Y
                        if Zmax < Z: Zmax = Z
                        if X < Xmin: Xmin = X
                        if Y < Ymin: Ymin = Y
                        if Z < Zmin: Zmin = Z

                    except UnboundLocalError:
                        Xmax = X
                        Ymax = Y
                        Zmax = Z
                        Xmin = X
                        Ymin = Y
                        Zmin = Z
                    
                    self.liste3D.append([X, Y, Z])
            self.listeCoo = (Xmax, Ymax , Zmax, Xmin, Ymin, Zmin)
            #-------------------------------------------Initialize le verticalSlider-------------------------------------------#
            self.AptLen = len(self.liste)
            self.verticalSlider.setMaximum(self.AptLen)
            #----------------------------------------Affiche les élement de la liste-----------------------------------------#
            self.InputTextEdit.clear()
            for g in range(self.NbrLigneAffiche):
                self.liste[g] = self.liste[g].replace("\r\n", "")
                self.InputTextEdit.append(self.liste[g])
               
            #--------------------------------------------------Referme le fichier-----------------------------------------------#
            fichier.close()
            self.progressBar.setValue(0)
        except IOError:
            pass
       
       
    """--------------------------------------------------------------------------------------------------Ouvrir Un Fichier------------------------------------------------------------------------------------------"""

    @pyqtSignature("")
    def on_actionOuvrir_activated(self):
        try:
            #--------------------------------Selection du Fichier, ouverture en lecture-----------------------------#
            filename=QFileDialog.getOpenFileName(self, "Explorateur de Fichier – Ouvrir un Fichier", "", "AptSource (*.aptsource)")
            fichier = open(filename, "r")
            self.Header()
            self.Ender()
            #----------------------------------Met la collection d ligne dans une liste--------------------------------#
            self.liste = fichier.readlines()
            self.progressBar.setMaximum(27)  
        
            #-------------------------------------------Initialize le verticalSlider-------------------------------------------#
            self.AptLen = len(self.liste)
            self.verticalSlider.setMaximum(self.AptLen)
            #---------------------------------------Affiche les élement de la liste------------------------------------------#
            self.InputTextEdit.clear()
            for g in range(self.NbrLigneAffiche):
                self.liste[g] = self.liste[g].replace("\r\n", "")
                self.InputTextEdit.append(self.liste[g])
                self.progressBar.setValue(self.progressBar.value()+1)
            #--------------------------------------------------Referme le fichier-----------------------------------------------#
            fichier.close()
            self.progressBar.setValue(0)
        except IOError:
            pass
    
       
        """--------------------------------------------------------------------------------------------------Enregistrer un fichier------------------------------------------------------------------------------------------"""
    @pyqtSignature("")
    def on_actionEnregistrer_activated(self):
        """
        Slot documentation goes here.
        """
        try:
            #--------------------------------Selection du Fichier, ouverture en Ecriture-----------------------------#
            filename=QFileDialog.getSaveFileName(self, "Explorateur de Fichier – Enregistrer un Fichier", "", "Ngc (*.ngc)")
            fichier = open(filename, "w")
            #-----------------------------Ajoute ligne à ligne chaque element de la liste----------------------------#
            for g in range(len(self.listeCalcul )):
                fichier.write(str(self.listeCalcul [g]) + "\n")
            #--------------------------------------------------Referme le fichier-----------------------------------------------#
            fichier.close()
        except IOError:
            pass
    
    """---------------------------------------------------------------------------------------------------------Quitter--------------------------------------------------------------------------------------------------------"""
    @pyqtSignature("")
    def on_actionQuitter_activated(self):
        """
        Slot documentation goes here.
        """
        self.close()
        
        """------------------------------------------------------------------------------------------------------Extraction-------------------------------------------------------------------------------------------------"""
    def Extraction(self, ligne,  Bol_Calcul):
        ligne = ligne.replace("GOTO", "")
        ligne = ligne.replace("/", "")
        self.liste = ligne.split(",")
        X = Decimal(self.liste[0])
        Y = Decimal(self.liste[1])
        Z = Decimal(self.liste[2])
        I = Decimal(self.liste[3])
        J = Decimal(self.liste[4])
        K = Decimal(self.liste[5])


        #------------------------------------Caclul C---------------------------------#
        if Bol_Calcul == False:
            if 0 < math.degrees(math.atan2(I, J)):
                self.Stock_C = 0
                formule = (math.fabs(math.degrees(math.atan2(I, J))))
                C = formule
            else:
                self.Stock_C = 360 - 2*(math.fabs(math.degrees(math.atan2(I, J))))
                formule = 360 - (math.fabs(math.degrees(math.atan2(I, J))))
                C = self.Stock_C
                
        else:
            
            if math.fabs(math.degrees(math.atan2(I, J))) <= math.fabs(math.degrees(math.atan2(self.I1, self.J1))):
                formule = 360 - math.fabs(math.degrees(math.atan2(I, J))) 
            
            if math.fabs(math.degrees(math.atan2(I, J))) > math.fabs(math.degrees(math.atan2(self.I1, self.J1))):
                formule = math.fabs(math.degrees(math.atan2(I, J))) 
        
            if 300 < math.fabs(formule - self.formule1):
                self.Stock_C = self.Stock_C + 360
            
            C = self.Stock_C + formule
        
        C = str(round(C, 3))
        self.formule1 = formule
        self.I1 = I
        self.J1 = J
        #------------------------------------Caclul A---------------------------------#
        A = math.degrees(math.atan2(-math.sqrt(I*I+J*J),  K))
        A = str(round(A, 3))
        #------------------------------------Caclul X---------------------------------#
        X = str(round(X, 3))
        #------------------------------------Caclul Y---------------------------------#
        Y = str(round(Y, 3))
        #------------------------------------Caclul Z---------------------------------#
        Z = str(round(Z, 3))
        if Bol_Calcul == False:
            return formule
        else:
            return ("X " + X + " Y " + Y + " Z " + Z + " A " + A + " C " + C)

