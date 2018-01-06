# -*- coding: utf-8 -*-

import Utils
from ctypes import *
from PIL import Image
import logging
import time
import numpy as np
import cv2


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        logging.info('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap


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

    @timing
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

    @timing
    def chemin_less_energy(self, energy_tab, orientation):
        """calcul le chemin d energie la plus faible"""
        logging.info("Processing path of minimum energy ...")
        lessEnergyPath = CDLL("./c_files/lessEnergyPath.so")
        lessEnergyPath.getPath.restype = POINTER(c_int)
        c_data =(c_int *len(energy_tab))(*energy_tab)
        tmp = lessEnergyPath.getPath(self.width, self.height, c_data, orientation)
        if orientation == 1:
            path = [tmp[i] for i in range(self.height)]
        else:
            path = [tmp[i] for i in range(self.width)]
        lessEnergyPath.free_p()
        logging.info("Done.")
        return path

    @timing
    def shrink_image(self, loop, orientation):
        img = self.img
        for i in range(loop):
            path = self.chemin_less_energy(self.energy_tab, orientation)
            tmp = self.img_data
            #debug_path(self.width, self.height, path, tmp)
            if orientation == 1:
                img = self.copyImage(tmp, path)
                self.update_values(self.width - 1, self.height, image_data=img)
            else:
                img = self.copyImageh(tmp, path)
                self.update_values(self.width, self.height - 1, image_data=img)
        self.gui.updateImage(img, self.width, self.height)

    @timing
    def copyImageh(self, tmp, path):
        h, w = self.height, self.width
        old_size = w * h

        newI = [0] * (w * (h - 1))
        energy_tab = self.energy_tab
        new_energy = [0] * (w * (h - 1))
        index = 0
        for i in range(0, w, 1):

            for j in range(0,path[index],w):
                newI[j] = tmp[j]
                new_energy[j] = energy_tab[j]

            for j in range(path[index]+w,old_size,w):
                npw = j-w
                newI[npw] = tmp[j]
                new_energy[npw] = energy_tab[j]
            index +=1

        self.energy_tab = new_energy
        return newI

    @timing
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

    @timing
    def detection(self):

        casc = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")

        cv_img = cv2.cvtColor(np.array(self.img), cv2.COLOR_RGB2BGR)
        img_gray = cv2.cvtColor(cv_img,cv2.COLOR_BGR2GRAY)
        faces = casc.detectMultiScale(img_gray,1.3,5)
        ww = self.width

        for x,y,w,h in faces:
            self.face_energy(ww,x,y,w,h)

    @timing
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

