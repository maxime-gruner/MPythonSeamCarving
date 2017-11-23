# -*- coding: utf-8 -*-

import Utils
from ctypes import *
import math
from PIL import Image
import logging
import time
from numpy.ctypeslib import ndpointer


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
        imgE = Image.new("L", (w, h))
        imgE.putdata(energy_tab)
        self.energy_tab = energy_tab
        imgE.show()
        logging.info("Done.")

    def chemin_less_energy(self):
        """calcul le chemin d energie la plus faible"""
        logging.info("Processing path of minimum energy ...")
        self.cost = [i for i in range(self.width * self.height)]
        for i in range(self.width):
            self.cost[i] = self.energy_tab[i]

        for j in range(0, self.height - 2):
            for i in range(0, self.width):
                if (i == self.width):
                    self.cost[j * self.width + i] = self.cost[j * self.width + i] + min(
                        self.cost[(j + 1) * self.width + i - 1], self.cost[(j + 1) * self.width + i])
                elif (i == 0):
                    self.cost[j * self.width + i] = self.cost[j * self.width + i] + min(
                        self.cost[(j + 1) * self.width + i], self.cost[(j + 1) * self.width + (i + 1)])
                else:
                    self.cost[j * self.width + i] = self.cost[j * self.width + i] + min(
                        self.cost[(j + 1) * self.width + i - 1], self.cost[(j + 1) * self.width + i],
                        self.cost[(j + 1) * self.width + (i + 1)])
        logging.info("Done.")

    def min_neighbour(self, cx, cy):
        x, y = cx, cy
        cv = self.cost[cy * self.width + cx]
        for i in range(-1, 2):
            if cv >= self.cost[(cy - 1) * self.width + i]:
                x, y = cx + i, cy - 1
                cv = self.cost[(cy - 1) * self.width + i]
        return cv, x, y

    def find_path(self):
        """recup le chemin en remontant le tableau cost """
        logging.info("Get the path from cost ...")
        self.path = [i for i in range(self.height)]
        current = math.inf
        k = 1
        for i in range(self.width):
            if current > self.cost[self.width * (self.height - 1) + i]:
                cx, cy = (i, (self.height))
        self.path[0] = cx, cy
        for i in range(self.height - 1, 0, -1):
            cv, cx, cy = self.min_neighbour(cx, i)
            self.path[k] = cx, cy
            k += 1
        logging.info("Path found")
        logging.info("Minimum path is %s" % self.path)
        res = [i for i in range((self.width-1)*self.height)]


    def shrink_image(self, widget):
        self.chemin_less_energy()
        self.find_path()
