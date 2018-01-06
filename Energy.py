# -*- coding: utf-8 -*-

import Utils
from ctypes import *
from PIL import Image
import logging
import numpy as np
import cv2



class Energy:
    def __init__(self, gui):
        self.gui = gui
        self.width = 0
        self.height = 0
        self.img = None
        self.times = 1
        self.energy_tab = []
        self.img_data = []
        self.intensity = []

        self.imgBW = []

    def calc_intensity(self):
        """calcul l intensite des pixel, la formule peut etre changée je pense"""
        logging.info("Processing intensity ...")
        self.imgBW = list(self.img.convert("L").getdata())
        logging.info("Done.")

    def update_values(self, width, height, image=None, image_data=None):
        self.width = width
        self.height = height

        if image:
            self.img = image
            self.calc_intensity()
            self.img_data = list(self.img.getdata())
        else:
            self.img_data = image_data

    @Utils.timing
    def calc_energy(self,imgBW):
        """calcul l energie de chaque pixel"""
        logging.info("Processing energy ...")
        gradient = CDLL("./c_files/gradient.so")
        gradient.calculate_energy.restype = POINTER(c_int)
        c_data = (c_int * len(imgBW))(*imgBW)
        w, h = self.width, self.height
        tmp = gradient.calculate_energy(w, h, c_data)
        energy_tab = [tmp[i] for i in range(0,w*h)]
        gradient.free_p()
        logging.info("Done.")
        return energy_tab

    @Utils.timing
    def chemin_less_energy(self, energy_tab):
        """calcul le chemin d energie la plus faible"""
        logging.info("Processing path of minimum energy ...")
        lessEnergyPath = CDLL("./c_files/lessEnergyPath.so")
        lessEnergyPath.getPath.restype = POINTER(c_int)

        c_data =(c_int *len(energy_tab))(*energy_tab)
        tmp = lessEnergyPath.getPath(self.width, self.height, c_data)
        path = [tmp[i] for i in range(self.height)]
        lessEnergyPath.free_p()
        logging.info("Done.")
        return path

    @Utils.timing
    def cheminNCSC(self, energy_tab):
        '''Autre méthode pour calculer le chemin, dans laquelle on ne calcul plus le cumul d'énergie, mais on choisi
        le pixel suivant juste en comparant sa valeur'''
        logging.info("Processing path of minimum energy ...")
        ncsc = CDLL("./c_files/energyPathNCSC.so")
        ncsc.getPath.restype = POINTER(c_int)
        c_data = (c_int *len(energy_tab))(*energy_tab)
        tmp = ncsc.getPath(self.width, self.height,c_data)
        path = [tmp[i] for i in range(self.height)]
        ncsc.free_p()
        logging.info("Done.")
        return path


    @Utils.timing
    def shrink_image(self, loop, orientation):
        img = self.img
        if orientation == 0:
            self.width, self.height = self.height, self.width
            self.energy_tab = Utils.rotate(self.energy_tab, self.width, self.height)
            self.img_data = Utils.rotate(self.img_data, self.width, self.height)
        for i in range(loop):
            path = self.chemin_less_energy(self.energy_tab)
            tmp = self.img_data
            img = self.copyImage(tmp, path)
            #debug_path(self.width, self.height, path, tmp)
            self.update_values(self.width-1, self.height, image_data=img)
        if orientation == 0:
            self.width, self.height = self.height, self.width
            img = Utils.invRotate(img, self.width, self.height)
            self.energy_tab = Utils.invRotate(self.energy_tab, self.width, self.height)
            self.img_data = img

        self.gui.updateImage(img, self.width, self.height)

    @Utils.timing
    def copyImage(self, tmp, path):
        h, w = self.height, self.width

        newI = []
        energy_tab = self.energy_tab
        new_energy = []

        for i in range(0,h):
            newI.extend(tmp[i*w:path[i]])
            newI.extend(tmp[path[i]+1:i*w+w])

            new_energy.extend(energy_tab[i * w:path[i]])
            new_energy.extend(energy_tab[path[i] + 1:i * w + w])
        self.energy_tab = new_energy
        return newI

    @Utils.timing
    def detection(self):

        casc = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")

        cv_img = cv2.cvtColor(np.array(self.img), cv2.COLOR_RGB2BGR)
        img_gray = cv2.cvtColor(cv_img,cv2.COLOR_BGR2GRAY)
        faces = casc.detectMultiScale(img_gray,1.3,5)
        ww = self.width

        for x,y,w,h in faces:
            self.face_energy(ww,x,y,w,h)

    @Utils.timing
    def face_energy(self,ww,x,y,w,h):
        for i in range(y,y+h):
            for j in range(x,x+w):
                self.energy_tab[i*ww+j] = 255



def debug_path(w, h, path, img):
    """fonction qui permet de visualiser le chemin qui sera supprimer"""
    ni = Image.new("RGB", (w, h))

    for p in path:
        img[p] = (255, 0, 0)
    ni.putdata(img)
    ni.show()

