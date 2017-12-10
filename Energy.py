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
        self.intensity = []
        self.energy_tab = []
        self.path = []
        self.imgBW = None

    @timing
    def calc_intensity(self):
        """calcul l intensite des pixel, la formule peut etre changée je pense"""
        logging.info("Processing intensity ...")
        self.imgBW = self.img.convert("L")
        logging.info("Done.")

    def update_values(self, width, height, name_img):
        self.width = width
        self.height = height

        self.energy_tab = []

        self.img = Image.open(name_img)
        self.calc_intensity()
        self.calc_energy()
        self.shrink_image()


    @timing
    def calc_energy(self):
        """calcul l energie de chaque pixel"""
        logging.info("Processing energy ...")
        gradient = CDLL("./c_files/gradient.so")
        data = [element for element in self.imgBW.getdata()]
        gradient.calculate_energy.restype = POINTER(c_int)
        c_data = (c_int * len(data))(*data)
        w, h = self.width, self.height
        tmp = gradient.calculate_energy(w, h, c_data)
        energy_tab = [tmp[i] for i in range(0,w*h)]
        gradient.free_p()
        self.energy_tab = energy_tab
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

    def shrink_image(self):
        self.chemin_less_energy()
        tmp = list(self.img.getdata())
        for e in self.path:
            tmp[e] = (0, 0, 0)
        self.gui.updateImage(tmp, self.width, self.height)


