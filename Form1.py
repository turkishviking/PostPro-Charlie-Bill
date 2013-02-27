# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QFileDialog,  QMessageBox
import Ui_APropo
from Ui_Form1 import Ui_MainWindow
import math
from decimal import Decimal
import Ui_test
import os
from PyQt4 import QtCore, QtGui
import OGL
import AudioPlayer

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    @pyqtSignature("")
    def on_pushButton_clicked(self):
        self.Formtest = QtGui.QWidget()
        self.uitest = Ui_test.Ui_Form()
        self.uitest.setupUi(self.Formtest,  self.listetest)
        self.Formtest.show()
        


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
        self.connect(self.InputTextEdit, QtCore.SIGNAL("scrol(int)"),  self.scrollInput)
        self.connect(self.TransformTextEdit, QtCore.SIGNAL("scrol(int)"),  self.scrollTransform)
        self.BoutonPrevusalisation.setEnabled(False)
        self.lineEdit.setText("0.5")
        self.vitesseCourrante = 0

    @pyqtSignature("")
    def on_BouttonEffacer_clicked(self):
        """
        Slot documentation goes here.
        """
        self.TransformTextEdit.clear()

        
    """ --------------------------------------------------------------------------------------------------------Initialise une fenetre OGL---------------------------------------------------------------------------"""
    @pyqtSignature("")
    def on_BoutonPrevusalisation_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            Dialog = QtGui.QWidget()
            di = OGL.MonDialog()
            di.setupUi(Dialog, self.liste3D, self.listeCoo,  self)
            reply = Dialog.show()
        except AttributeError:
            pass
    
    """-----------------------------------------------------------------------------------------\\\\\\\\\\----------Calcul-----------////////----------------------------------------------------------------------------"""
    @pyqtSignature("")
    def on_BouttonCalcul_clicked(self):
        """
        Slot documentation goes here.
        """
        self.TransformTextEdit.clear
        self.Mode = 0
        self.listetest=[]
        self.Stock_C = 0
        self.listeCalcul = []
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(len(self.liste))
        #------------------------------------------------------Ajoute le Header----------------------------------------------#
        d = self.HeadertextEdit.toPlainText()
        listeheader = d.split("\n")
        for a in listeheader:
            self.listeCalcul.append(a)
        

        #---------------------------------\\\\\\------Traitement des données------///////------------------------------#
        #-----------------------------------------------------Prend l'outil----------------------------------------------------#
     
        listeT = self.liste
        for ligne in listeT:
            self.progressBar.setValue( self.progressBar.value()+1)
            if "LOADTL/" in ligne:

                self.listeCalcul .append("T" + ligne.replace("LOADTL/", "") + " G43")
                self.listeCalcul .append("M6")
                self.listeCalcul .append("G1 F1000")

                
            if "FEDRAT/" in ligne:   
                if self.checkBox.isChecked() == False:
                    ligne=ligne.replace("FEDRAT/", "").replace(" ", "")
                    ligne=ligne.replace(",MMPM", "")
                    self.listeCalcul .append("G1 F" + (ligne))
                    self.vitesse = float(ligne)

                    
            #----------------------------------------------------Extraction-----------------------------------------------------#
            if "GOTO" in ligne:

                self.listeCalcul .append(self.Extraction(ligne))
            #-------------------------------------------------Ajout de Ender---------------------------------------------------#
        d = self.EnderTextEdit.toPlainText()
        listeEnder = d.split("\n")
        for a in listeEnder:
            self.listeCalcul.append(a)
        #-------------------------------------------Affiche les  élement de la liste-------------------------------------#
        self.verticalSlider_2.setMaximum(len(self.listeCalcul))
        self.AfficheTransform()

    """--------------------------------------------------------------------------------------Header, Ender------------------------------------------------------------------------------------------------------"""

    #-------------------------------------------------------Header-----------------------------------------------------#
    def Header(self):
        self.HeadertextEdit.clear()
        self.HeadertextEdit.append("%")
        self.HeadertextEdit.append(self.unit)
        self.HeadertextEdit.append(self.deplacement)
        self.HeadertextEdit.append(self.PlandeTravail)
        self.HeadertextEdit.append(self.coordonnees)
        #-------------------------------------Vitesse Rapide pour Simulation--------------------------------------#
        if self.checkBox.isChecked() == True:
            self.HeadertextEdit.append("G0")
            

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
        
    """----------------------------------------------------------------------------------------Affichage des TextBox----------------------------------------------------------------------------------------------------------"""
    def AfficheInput(self):
        try:
            self.InputTextEdit.clear()
            for g in range(self.verticalSlider.value(), self.verticalSlider.value()+ self.NbrLigneAffiche):
                self.liste[g] = self.liste[g].replace("\r\n", "")
                self.InputTextEdit.append(self.liste[g])
        except (AttributeError,  IndexError):
            pass
            
    def AfficheTransform(self):
        try:
            self.TransformTextEdit.clear()
            for g in range(self.verticalSlider_2.value(), self.verticalSlider_2.value()+ self.NbrLigneAffiche):
                self.listeCalcul [g] = str(self.listeCalcul [g]).replace("\r\n", "")
                self.TransformTextEdit.append(self.listeCalcul [g])
        except (AttributeError,  IndexError):
            pass
        
        
    """----------------------------------------------------------------------------------------------------Mise a jour quand Resize----------------------------------------------------------------------------------------------"""
    def resizeEvent(self, event):
        self.NbrLigneAffiche = int(self.InputTextEdit.height()/13.5)
        self.AfficheInput()
        self.AfficheTransform()
             
    """---------------------------------------------------------------------------------------------------------Scroll des TextEdit------------------------------------------------------------------------------------------------------------"""
    def scrollInput(self,  intArg):
            self.verticalSlider.setValue(self.verticalSlider.value() -  intArg)
    def scrollTransform(self,  intArg):
            self.verticalSlider_2.setValue(self.verticalSlider_2.value() -  intArg)
        

      
    """--------------------------------------------------------------------------------------------------Gestion des slider------------------------------------------------------------------------------------------"""
    @pyqtSignature("int")
    def on_verticalSlider_valueChanged(self, value):
        """
        Slot documentation goes here.
        """
        try:
            self.AfficheInput()
            self.spinBox.setMaximum(len(self.liste))
            self.spinBox.setValue(self.verticalSlider.value())
        except AttributeError:
          pass
            
    @pyqtSignature("int")
    def on_verticalSlider_2_valueChanged(self, value):
        """
        Slot documentation goes here.
        """
        try:
            self.AfficheTransform()
            self.spinBox_2.setMaximum(len(self.liste))
            self.spinBox_2.setValue(self.verticalSlider_2.value())
        except AttributeError:
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
        
    
    @pyqtSignature("")
    def on_actionA_Propos_activated(self):
        """
        Slot documentation goes here.
        """
        #--------------------------------------Ouvre la fenetre Ui a Propos--------------------------------#
        self.Dialog = QtGui.QWidget()
        self.ui = Ui_APropo.Ui_Dialog()
        self.ui.setupUi(self.Dialog)
        self.Dialog.show()
    
    @pyqtSignature("")
    def on_actionLecteur_Audio_activated(self):
        """
        Slot documentation goes here.
        """
        self.W = QtGui.QWidget()
        self.aud = AudioPlayer.AudioPlayer()
        self.aud.show()
        

    
    
    """--------------------------------------------------------------------------------------------------Ouvrir un fichier et prévisualiser-----------------------------------------------------------------------------------------"""
    @pyqtSignature("")
    def  on_actionOuvrir_et_pr_visualiser_activated(self):
        """
        Slot documentation goes here.
        """
        self.BoutonPrevusalisation.setEnabled(True)
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
            listeT = self.liste
            for ligne in listeT:
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
            self.AfficheInput()
     
               
            #--------------------------------------------------Referme le fichier-----------------------------------------------#
            fichier.close()
            self.progressBar.setValue(0)
        except (IOError, UnboundLocalError):
            self.BoutonPrevusalisation.setEnabled(False)
       
       
    """--------------------------------------------------------------------------------------------------Ouvrir Un Fichier------------------------------------------------------------------------------------------"""

    @pyqtSignature("")
    def on_actionOuvrir_activated(self):
        self.BoutonPrevusalisation.setEnabled(False)
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
            self.AfficheInput()
    
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
            if ".ngc" in filename:
                ext = ""
            else:
                ext = ".ngc"
            fichier = open(filename + ext, "w")
            #-----------------------------Ajoute ligne à ligne chaque element de la liste----------------------------#
            for g in range(len(self.listeCalcul )):
                fichier.write(str(self.listeCalcul [g]) + "\n")
            #--------------------------------------------------Referme le fichier-----------------------------------------------#
            fichier.close()
            QMessageBox.warning(None, "Enregistrement", "Youpi!!!! pov'con!")
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
    def Extraction(self, ligne):
        ligne = ligne.replace("GOTO", "")
        ligne = ligne.replace("/", "")
        self.listeValeur = ligne.split(",")
        X = Decimal(self.listeValeur[0])
        Y = Decimal(self.listeValeur[1])
        Z = Decimal(self.listeValeur[2])
        
                    
        #------------------------------------Caclul X---------------------------------#
        X = str(round(X, 3))
        #------------------------------------Caclul Y---------------------------------#
        Y = str(round(Y, 3))
        #------------------------------------Caclul Z---------------------------------#
        Z = str(round(Z, 2))
        
        
        try:
            I = Decimal(self.listeValeur[3])
            J = Decimal(self.listeValeur[4])
            K = Decimal(self.listeValeur[5])

            #------------------------------------Caclul C---------------------------------#
            try:
                if 150 < math.degrees(math.atan2(self.J1, self.I1)):
                    if -150 > math.degrees(math.atan2(J, I)): #----==> tourne à droite, Incrémente stock C par ajouts, Passe en mode 1
                        self.Stock_C = self.Stock_C +360

                if -150 > math.degrees(math.atan2(self.J1, self.I1)):
                    if 150 < math.degrees(math.atan2(J, I)): #----==> tourne à gauche, Décrémente stock C par soustraction, Passe en mode 1
                        self.Stock_C = self.Stock_C -360    

                C = (self.Stock_C + math.degrees(math.atan2(J, I)))
                C = str(round(C, 3))
                #------------------------------------Caclul B---------------------------------#
                B = math.degrees(math.atan2(K,  math.sqrt(I*I+J*J))) - 90
                B = str(round(B, 3))
                
            except AttributeError:
                C = math.degrees(math.atan2(J, I))  
                C = str(round(C, 3))
                #------------------------------------Caclul B---------------------------------#
                B =  math.degrees(math.atan2(K,  math.sqrt(I*I+J*J))) - 90
                B = str(round(B, 3))

                
            self.I1 = I
            self.J1 = J
            


            return ("X " + X + " Y " + Y + " Z " + Z + " B " + B + " C " + C)

        except (IndexError,  AttributeError):
            return ("X " + str(X) + " Y " + str(Y) + " Z " + str(Z), )


        
        #-------------------------------test--------------------------------
        self.listetest.append(" -Atan2: " + str(round(math.degrees(math.atan2(I, J)), 3)) + "  -ABS: " + str(round(math.fabs(math.degrees(math.atan2(I, J))), 3)) + "  Formule: " + C  +"  " + str(self.Mode)  )

