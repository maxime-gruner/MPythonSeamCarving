# -*- coding: utf-8 -*-

import Utils
from ctypes import *
import numpy as np
from PIL import Image
import logging
import time


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
        self.img_data = []
        self.intensity = []
        self.energy_tab = []
        self.path = []
        self.imgBW = []

    @timing
    def calc_intensity(self):
        """calcul l intensite des pixel, la formule peut etre changée je pense"""
        logging.info("Processing intensity ...")
        self.imgBW = list(self.img.convert("L").getdata())
        logging.info("Done.")

    def update_values(self, width, height, image=None, image_data=None):
        self.width = width
        self.height = height

        self.energy_tab = []
        if image:
            self.img = image
            self.calc_intensity()
            self.img_data = list(self.img.getdata())
        else:
            self.img_data = image_data
        self.calc_energy()




    @timing
    def calc_energy(self):
        """calcul l energie de chaque pixel"""
        logging.info("Processing energy ...")
        gradient = CDLL("./c_files/gradient.so")
        gradient.calculate_energy.restype = POINTER(c_int)
        c_data = (c_int * len(self.imgBW))(*self.imgBW)
        w, h = self.width, self.height
        tmp = gradient.calculate_energy(w, h, c_data)
        self.energy_tab = [tmp[i] for i in range(0,w*h)]
        gradient.free_p()
        logging.info("Done.")

    @timing
    def chemin_less_energy(self):
        """calcul le chemin d energie la plus faible"""
        logging.info("Processing path of minimum energy ...")
        lessEnergyPath = CDLL("./c_files/lessEnergyPath.so")
        lessEnergyPath.getPath.restype = POINTER(c_int)
        c_data =(c_int *len(self.energy_tab))(*self.energy_tab)
        tmp = lessEnergyPath.getPath(self.width, self.height, c_data)
        self.path = [tmp[i] for i in range(0,self.height)]
        lessEnergyPath.free_p()
        logging.info("Done.")

    @timing
    def shrink_image(self, loop):
        img = self.img
        for i in range(loop):
            self.chemin_less_energy()
            tmp = self.img_data
            for e in self.path:
                tmp[e] = (0, 0, 0)
            img = self.copyImage(tmp)
            self.update_values(self.width-1, self.height, image_data=img)

        self.gui.updateImage(img, self.width, self.height)


    def copyImage(self,tmp):
        nw = self.width -1
        newI = [ 0 for i in range((nw)*self.height)]
        newBW = [ 0 for i in range((nw)*self.height)]
        index = 0
        for i in range(0,self.height):
            j2 = 0
            for j in range(0,self.width):
                if index == len(self.path):
                    for k in range(j,self.width):
                        newI[nw*i+j2] = tmp[self.width*i+k] #permet d avoir les dernier pixel, sinon on a une ligne noir a la fin
                        newBW[nw*i+j2] = self.imgBW[self.width*i+k]
                        j2 = j2 + 1
                    return newI
                if i*self.width+j != self.path[index]:
                    newI[nw*i+j2] = tmp[self.width*i+j]
                    newBW[nw*i+j2] = self.imgBW[self.width*i+j]

                    j2 = j2+1
                else:
                    index = index + 1
        self.imgBW = newBW
        return newI

