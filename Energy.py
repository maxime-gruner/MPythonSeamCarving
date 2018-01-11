# -*- coding: utf-8 -*-
import Utils
from ctypes import *
from PIL import Image
import logging
import numpy as np
import cv2
from operator import itemgetter



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


    def calc_energy_hog(self, imgBW):
        """calcul l energie de chaque pixel"""
        logging.info("Processing energy ...")
        gradient = CDLL("./c_files/gradient.so")
        gradient.calculate_energy_hog.restype = POINTER(c_int)
        c_data = (c_int * len(imgBW))(*imgBW)
        w, h = self.width, self.height
        tmp = gradient.calculate_energy_hog(w, h, c_data)
        energy_tab = [tmp[i] for i in range(0, w * h)]
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
    def cheminNCSC2(self, energy_tab,limit):
        '''Autre méthode pour calculer le chemin, dans laquelle on ne calcul plus le cumul d'énergie, mais on choisi
        le pixel suivant juste en comparant sa valeur'''
        logging.info("Processing path of minimum energy ...")
        path = self.getNCSCpath(energy_tab, self.width, self.height,limit)
        logging.info("Done.")
        return path

    @Utils.timing
    def shrink_image(self, loop, type ,orientation):
        img = self.img
        if orientation == 0:
            self.width, self.height = self.height, self.width
            self.energy_tab = Utils.rotate(self.energy_tab, self.width, self.height)
            self.img_data = Utils.rotate(self.img_data, self.width, self.height)
        i=0
        while i < loop:
            decrement = 1
            if type == 0:
                path = self.chemin_less_energy(self.energy_tab)
                tmp = self.img_data
                img = self.copyImage(tmp, path)
                i+=decrement
            elif type == 1:
                path = self.cheminNCSC2(self.energy_tab,loop-i)
                decrement = int((len(path)/self.height))
                i += decrement
                tmp = self.img_data
                #debug_path(self.width, self.height, path, tmp)
                img = self.copyImage(tmp, path)
            self.update_values(self.width-decrement, self.height, image_data=img)
        if orientation == 0:
            self.width, self.height = self.height, self.width
            img = Utils.invRotate(img, self.width, self.height)
            self.energy_tab = Utils.invRotate(self.energy_tab, self.width, self.height)
            self.img_data = img

        self.gui.updateImage(img, self.width, self.height)


    @Utils.timing
    def copyImage(self, tmp, path):

        newI = []
        energy_tab = self.energy_tab
        new_energy = []
        prevpos=0

        for i in path:
            newI.extend(tmp[prevpos:i])

            new_energy.extend(energy_tab[prevpos:i])
            prevpos = i+1

        newI.extend(tmp[prevpos:])

        new_energy.extend(energy_tab[prevpos:])
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


    def getNCSCpath(self, data, width, height, limit):
        tab = [(0, 0)] * (width * height)
        l = []
        for i in range(1, width - 1):
            tab[i] = (data[i], i)
            l.append(i)
        for i in range(height - 1):
            newl = []
            for j in l:
                bottom_pix = j + width
                bm1, b, bp1 = data[bottom_pix - 1], data[bottom_pix], data[bottom_pix + 1]
                if bm1 < b and bm1 < bp1:
                    sval, parent = tab[bottom_pix - 1]
                    pixval, pixparent = tab[j]
                    if parent != 0:
                        if sval > bm1 + pixval:
                            tab[bottom_pix - 1] = (bm1 + pixval, j)
                    else:
                        tab[bottom_pix - 1] = (bm1 + pixval, j)
                        newl.append(bottom_pix - 1)

                elif bp1 < b:
                    sval, parent = tab[bottom_pix + 1]
                    pixval, pixparent = tab[j]
                    if parent != 0:
                        if sval > bp1 + pixval:
                            tab[bottom_pix + 1] = (bp1 + pixval, j)
                    else:
                        tab[bottom_pix + 1] = (bp1 + pixval, j)
                        newl.append(bottom_pix + 1)

                else:
                    sval, parent = tab[bottom_pix]
                    pixval, pixparent = tab[j]
                    if parent != 0:
                        if sval > b + pixval:
                            tab[bottom_pix] = (b + pixval, j)
                    else:
                        tab[bottom_pix] = (b + pixval, j)
                        newl.append(bottom_pix)
            l = newl
        tmp = [tab[i] for i in l]
        tmp = sorted(tmp, key=itemgetter(0))
        min = tmp[0][0]
        offset = int(min + int(min * 50 / 100))
        res = []
        nbadd = 0
        for i in tmp:
            if i[0] < offset and nbadd < limit:
                nbadd += 1
                res.append(i[1] + width)
                res.append(i[1])
                prevpos = i[1]
                for n in range(height - 2):
                    val, pos = tab[prevpos]
                    res.append(pos)
                    prevpos = pos
            else:
                break
        res.sort()
        return res


def debug_path(w, h, path, img):
    """fonction qui permet de visualiser le chemin qui sera supprimer"""
    ni = Image.new("RGB", (w, h))

    for p in path:
        img[p] = (255, 0, 0)
    ni.putdata(img)
    ni.show()

