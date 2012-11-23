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
    global AptLen
    global liste
    global listeCalcul
    global listeHeader
    global I1
    global J1
    global formule1
    global Stock_C
    global liste3D
    global listeCoo
    global listeValeur
    global unit
    global deplacement
    global PlandeTravail
    global coordonnees
    
    
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        global unit
        global deplacement
        global PlandeTravail
        global coordonnees
        unit = "G21"
        deplacement = "G90"
        PlandeTravail = "G17"
        coordonnees = "G54"
        
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
        global liste3D
        global listeCoo
        Dialog = QtGui.QDialog()
        di = OGL.MonDialog()
        di.setupUi(Dialog, liste3D, listeCoo,  self)
        reply = Dialog.exec_()

    
    """-----------------------------------------------------------------------------------------\\\\\\\\\\----------Calcul-----------////////----------------------------------------------------------------------------"""
    @pyqtSignature("")
    def on_BouttonCalcul_clicked(self):
        """
        Slot documentation goes here.
        """
        global liste
        global listeCalcul
        global listeHeader
        global Stock_C 
        global liste3D
        liste3D = []
        Stock_C = 0
        listeCalcul = []
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(len(liste))
        Bol_Calcul = False
        #-------------------------------------Vitesse Rapide pour Simulation--------------------------------------#
        if self.checkBox.isChecked() == True:
            listeHeader.append("G1 " + "F10000000000")
        #---------------------------------\\\\\\------Traitement des données------///////------------------------------#
        #-----------------------------------------------------Prend l'outil----------------------------------------------------#
        
        for ligne in liste:
            self.progressBar.setValue( self.progressBar.value()+1)
            if "LOADTL/" in ligne:
                listeCalcul.append("M5")
                listeCalcul.append("T" + ligne.replace("LOADTL/", "") + " G43")
                listeCalcul.append("M6")
                listeCalcul.append("M3")
                listeCalcul.append("M0")
                
            if self.checkBox.isChecked() == False:
                if "FEDRAT/ " in ligne:
                    ligne=ligne.replace("FEDRAT/ ", "")
                    ligne=ligne.replace(",MMPM", "")
                    listeCalcul.append("G1 F" + (ligne))
                    
            #----------------------------------------------------Extraction-----------------------------------------------------#
            if "GOTO" in ligne:
                listeCalcul.append(self.Extraction(ligne,  Bol_Calcul))
                Bol_Calcul = True

        #---------------------------------Affiche les 28 premier élement de la liste-----------------------------#
        self.verticalSlider_2.setMaximum(len(listeCalcul))
        try:
            for g in range(28):
                listeCalcul[g]=str(listeCalcul[g]).replace("\r\n", "")
                self.progressBar.setValue(self.progressBar.value()+1)
                self.TransformTextEdit.append(listeCalcul[g])
        except (NameError,  IndexError):
            pass
            
    """--------------------------------------------------------------------------------------Header, Ender------------------------------------------------------------------------------------------------------"""

    #-------------------------------------------------------Header-----------------------------------------------------#
    def Header(self):
        global unit
        global deplacement
        global PlandeTravail
        global coordonnees
        self.HeadertextEdit.clear()
        self.HeadertextEdit.append("%")
        self.HeadertextEdit.append(unit)
        self.HeadertextEdit.append(deplacement)
        self.HeadertextEdit.append(PlandeTravail)
        self.HeadertextEdit.append(coordonnees)

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
        global unit
        if str(p0) == "mm":
            unit = "G21"
        else:
            unit = "G20"
        self.Header()
    
    @pyqtSignature("QString")
    def on_comboBoxType_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        """
        global deplacement
        if str(p0) == "Absolues":
            deplacement = "G90"
        else:
            deplacement = "G91"
        self.Header()
    
    @pyqtSignature("QString")
    def on_comboBoxPlan_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        """
        global PlandeTravail
        if str(p0) == "XY":
            PlandeTravail = "G17"
        elif str(p0) == "XZ":
            PlandeTravail = "G18"
        else:
            PlandeTravail = "G19"
        self.Header()
    
    @pyqtSignature("QString")
    def on_comboBoxCoordonees_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        """
        global coordonnees
        if str(p0) == "Origine piece 1":
            coordonnees = "G54"
        if str(p0) == "Origine piece 2":
            coordonnees = "G55"
        if str(p0) == "Origine piece 3":
            coordonnees = "G56"
        if str(p0) == "Origine piece 4":
            coordonnees = "G57"
        if str(p0) == "Origine piece 5":
            coordonnees = "G58"
        if str(p0) == "Origine piece 6":
            coordonnees = "G59"
        if str(p0) == "Origine piece 7":
            coordonnees = "G59.1"
        if str(p0) == "Origine piece 8":
            coordonnees = "G59.2"
        if str(p0) == "Origine piece 9":
            coordonnees = "G59.3"
        self.Header()
        
    """--------------------------------------------------------------------------------------------------Gestion des slider------------------------------------------------------------------------------------------"""
    @pyqtSignature("int")
    def on_verticalSlider_valueChanged(self, value):
        """
        Slot documentation goes here.
        """
        global liste
        try:
            self.InputTextEdit.clear()
            for g in range(self.verticalSlider.value(), self.verticalSlider.value()+28):
                liste[g] = liste[g].replace("\r\n", "")
                self.InputTextEdit.append(liste[g])
            self.spinBox.setMaximum(len(liste))
            self.spinBox.setValue(self.verticalSlider.value())
        except (NameError,  IndexError):
            pass
            
    @pyqtSignature("int")
    def on_verticalSlider_2_valueChanged(self, value):
        """
        Slot documentation goes here.
        """
        global listeCalcul
        try:
            self.TransformTextEdit.clear()
            for g in range(self.verticalSlider_2.value(), self.verticalSlider_2.value()+28):
                listeCalcul[g] = str(listeCalcul[g]).replace("\r\n", "")
                self.TransformTextEdit.append(listeCalcul[g])
            self.spinBox_2.setMaximum(len(listeCalcul))
            self.spinBox_2.setValue(self.verticalSlider_2.value())
        except (NameError,  IndexError):
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
        global AptLen
        global liste
        global liste3D
        global listeValeur
        global listeCoo

        #--------------------------------Selection du Fichier, ouverture en lecture-----------------------------#
        filename=QFileDialog.getOpenFileName(self, "Explorateur de Fichier – Ouvrir un Fichier", "", "AptSource (*.aptsource)")
        fichier = open(filename, "r")
        self.Header()
        self.Ender()
        #----------------------------------Met la collection d ligne dans une liste--------------------------------#
        liste = fichier.readlines()
        self.progressBar.setMaximum(len(liste))
        #----------------------------------Extrait les coordonnées pour openGL--------------------------------#
        liste3D=[]
        listeCoo=[]
        
        for ligne in liste:
            self.progressBar.setValue(self.progressBar.value()+1)
            if "GOTO" in ligne:
                ligne = ligne.replace("GOTO", "")
                ligne = ligne.replace("/", "")
                listeValeur = ligne.split(",")
                X = Decimal(listeValeur[0])
                Y = Decimal(listeValeur[1])
                Z = Decimal(listeValeur[2])
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
                
                liste3D.append([X, Y, Z])
        listeCoo = (Xmax, Ymax , Zmax, Xmin, Ymin, Zmin)
        #-------------------------------------------Initialize le verticalSlider-------------------------------------------#
        AptLen = len(liste)
        self.verticalSlider.setMaximum(AptLen)
        #---------------------------------Affiche les 28 premier élement de la liste-----------------------------#
        self.InputTextEdit.clear()
        for g in range(28):
            liste[g] = liste[g].replace("\r\n", "")
            self.InputTextEdit.append(liste[g])
           
        #--------------------------------------------------Referme le fichier-----------------------------------------------#
        fichier.close()
        self.progressBar.setValue(0)
       
       
    """--------------------------------------------------------------------------------------------------Ouvrir Un Fichier------------------------------------------------------------------------------------------"""

    @pyqtSignature("")
    def on_actionOuvrir_activated(self):
       
        global liste
        global Aptlen
        
        #--------------------------------Selection du Fichier, ouverture en lecture-----------------------------#
        filename=QFileDialog.getOpenFileName(self, "Explorateur de Fichier – Ouvrir un Fichier", "", "AptSource (*.aptsource)")
        fichier = open(filename, "r")
        self.Header()
        self.Ender()
        #----------------------------------Met la collection d ligne dans une liste--------------------------------#
        liste = fichier.readlines()
        self.progressBar.setMaximum(27)  
    
        #-------------------------------------------Initialize le verticalSlider-------------------------------------------#
        AptLen = len(liste)
        self.verticalSlider.setMaximum(AptLen)
        #---------------------------------Affiche les 28 premier élement de la liste-----------------------------#
        self.InputTextEdit.clear()
        for g in range(28):
            liste[g] = liste[g].replace("\r\n", "")
            self.InputTextEdit.append(liste[g])
            self.progressBar.setValue(self.progressBar.value()+1)
        #--------------------------------------------------Referme le fichier-----------------------------------------------#
        fichier.close()
        self.progressBar.setValue(0)
    
       
        """--------------------------------------------------------------------------------------------------Enregistrer un fichier------------------------------------------------------------------------------------------"""
    @pyqtSignature("")
    def on_actionEnregistrer_activated(self):
        """
        Slot documentation goes here.
        """
        global liste
        #--------------------------------Selection du Fichier, ouverture en Ecriture-----------------------------#
        filename=QFileDialog.getSaveFileName(self, "Explorateur de Fichier – Enregistrer un Fichier", "", "Ngc (*.ngc)")
        fichier = open(filename, "w")
        #-----------------------------Ajoute ligne à ligne chaque element de la liste----------------------------#
        for g in range(len(listeCalcul)):
            fichier.write(str(listeCalcul[g]) + "\n")
        #--------------------------------------------------Referme le fichier-----------------------------------------------#
        fichier.close()
    
    """---------------------------------------------------------------------------------------------------------Quitter--------------------------------------------------------------------------------------------------------"""
    @pyqtSignature("")
    def on_actionQuitter_activated(self):
        """
        Slot documentation goes here.
        """
        self.close()
        
        """------------------------------------------------------------------------------------------------------Extraction-------------------------------------------------------------------------------------------------"""
    def Extraction(self, ligne,  Bol_Calcul):
        global I1
        global J1
        global formule1
        global Stock_C

        ligne = ligne.replace("GOTO", "")
        ligne = ligne.replace("/", "")
        liste = ligne.split(",")
        X = Decimal(liste[0])
        Y = Decimal(liste[1])
        Z = Decimal(liste[2])
        I = Decimal(liste[3])
        J = Decimal(liste[4])
        K = Decimal(liste[5])


        #------------------------------------Caclul C---------------------------------#
        if Bol_Calcul == False:
            if 0 < math.degrees(math.atan2(I, J)):
                Stock_C = 0
                formule = (math.fabs(math.degrees(math.atan2(I, J))))
                C = formule
            else:
                Stock_C = 360 - 2*(math.fabs(math.degrees(math.atan2(I, J))))
                formule = 360 - (math.fabs(math.degrees(math.atan2(I, J))))
                C = Stock_C
                
        else:
            
            if math.fabs(math.degrees(math.atan2(I, J))) <= math.fabs(math.degrees(math.atan2(I1, J1))):
                formule = 360 - math.fabs(math.degrees(math.atan2(I, J))) 
            
            if math.fabs(math.degrees(math.atan2(I, J))) > math.fabs(math.degrees(math.atan2(I1, J1))):
                formule = math.fabs(math.degrees(math.atan2(I, J))) 
        
            if 300 < math.fabs(formule - formule1):
                Stock_C = Stock_C + 360
            
            C = Stock_C + formule
        
        C = str(round(C, 3))
        formule1 = formule
        I1 = I
        J1 = J
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

