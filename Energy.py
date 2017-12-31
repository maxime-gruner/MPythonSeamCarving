# -*- coding: utf-8 -*-

import Utils
from ctypes import *
from PIL import Image
import logging
import time
import numpy as np


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
    def chemin_less_energy(self,energy_tab):
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

    @timing
    def shrink_image(self, loop):
        img = self.img
        energy_tab = self.calc_energy(self.imgBW)

        for i in range(loop):
            path = self.chemin_less_energy(energy_tab)
            tmp = self.img_data

            img = self.copyImage(tmp,path)

            self.update_values(self.width-1, self.height, image_data=img)
        self.gui.updateImage(img, self.width, self.height)



    @timing
    def copyImage(self, tmp, path):
        h, w = self.height, self.width
        old_size = w*h
        newI = []
        append = newI.append
        index = 0
        last = path[-1]

        for i in range(last):
            elem = tmp[i]
            if path[index] == i:
                index += 1
            else:
                append(elem)
        for i in range(last+1,old_size): # copie la derniere ligne
            append(tmp[i])
        return newI



