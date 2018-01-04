# -*- coding: utf-8 -*-

import Utils
from ctypes import *
from PIL import Image
import logging
import time




class element():
    def __init__(self, val, index, pindex=None):
        self.val = val
        self.index = index
        self.pindex = pindex


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        logging.info('%s function took %0.3f ms' % (f.__name__, (time2 - time1) * 1000.0))
        return ret

    return wrap


def min_element(x, y):
    a, ai, b, bi = x.val, x.index, y.val, y.index
    if a < b:
        return a, ai
    else:
        return b, bi


def min_element3(x, y, z):
    a, ai, b, bi, c, ci = x.val, x.index, y.val, y.index, z.val, z.index
    if a < b:
        if a < c:
            return a, ai
        else:
            return c, ci
    else:
        if b < c:
            return b, bi
        else:
            return c, ci


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
    def calc_energy(self, imgBW):
        """calcul l energie de chaque pixel"""
        logging.info("Processing energy ...")
        gradient = CDLL("./c_files/gradient.so")
        gradient.calculate_energy.restype = POINTER(c_int)
        c_data = (c_int * len(imgBW))(*imgBW)
        w, h = self.width, self.height
        tmp = gradient.calculate_energy(w, h, c_data)
        energy_tab = [tmp[i] for i in range(0, w * h)]
        gradient.free_p()
        logging.info("Done.")
        return energy_tab

    '''
    @timing
    def chemin_less_energy(self,energy_tab,loop):
        """calcul le chemin d energie la plus faible"""
        logging.info("Processing path of minimum energy ...")
        lessEnergyPath = CDLL("./c_files/lessEnergyPath.so")
        lessEnergyPath.processType.restype = ELEMENT
        c_data =(c_int *len(energy_tab))(*energy_tab)
        path = []
        map_energy = lessEnergyPath.processPath(self.width, self.height, c_data)
        for j in range(loop):
            tmp_path = lessEnergyPath.getMinPath(self.width,self.height)
            path = [path.append(tmp_path[i]) for i in range(self.height)]
        #lessEnergyPath.free_p()
        logging.info("Done.")
        return path
    '''

    @timing
    def process_path(self, w, h, energy_tab, loop):
        """Calcul tout les seams d energie"""
        logging.info("Processing path ...")
        min3 = min_element3
        min2 = min_element

        seams = [element(0, i) for i in range(h * w)]
        it_seams = iter(seams)
        it_energy = iter(energy_tab)

        for i in range(w):  # init 1ere ligne
            curr = next(it_seams)
            e = next(it_energy)
            curr.val = e

        for i in range(1, h):

            wi = w * i
            top_line = wi - w
            nw = w - 1
            e = next(it_energy)

            m, i2 = min2(seams[top_line], seams[top_line + 1])
            curr = next(it_seams)
            curr.val = m + e
            curr.pindex = i2
            for k in range(1, nw):
                t = top_line + k
                e = next(it_energy)
                m, i2 = min3(seams[t - 1], seams[t], seams[t + 1])

                curr = next(it_seams)
                curr.val = m + e
                curr.pindex = i2

            e = next(it_energy)
            m, i2 = min2(seams[top_line + nw - 1], seams[top_line + nw])
            curr = next(it_seams)
            curr.val = m + e
            curr.pindex = i2
        logging.info("Processing done ...")
        return seams

    @timing
    def get_min_path(self, w, h, seams, energy_tab):
        min = 9999999
        last = w * (h - 1)
        path = []

        for i in range(w):
            tmp = last + i
            if seams[tmp].val < min:
                save = tmp
                min = seams[tmp].val

        path.append(save)
        curr = seams[save]
        for i in range(h - 2, -1, -1):
            curr.val = 9999999
            old = curr
            k = old.index
            if k % w == 0: #met a jour les index en prenant l energie voisine la moins forte
                m, oldi = min_element(seams[k - w], seams[k - w + 1])
            elif k % w == w - 1:
                m, oldi = min_element(seams[k - w - 1], seams[k - w])
            else:
                m, oldi = min_element3(seams[k - w - 1], seams[k - w], seams[k - w + 1])
            old.pindex = oldi

            curr = seams[curr.pindex]
            path.append(curr.index)
        return path

    @timing
    def shrink_image(self, loop):
        img = self.img
        process_path = self.process_path
        get_min_path = self.get_min_path
        copyImage = self.copyImage
        update_values = self.update_values
        for i in range(loop):
            w, h = self.width, self.height
            energy_tab = self.energy_tab

            if i % 7 == 0: #peut deformer un peu l image si trop elever
                seams = process_path(w, h, energy_tab, loop)
            tmp = self.img_data
            path = get_min_path(w, h, seams, energy_tab)
            path.reverse()

            img = copyImage(tmp, path, w, h)
            update_values(self.width - 1, self.height, image_data=img)
            #debug_path(w, h, path, tmp)

        self.gui.updateImage(img, self.width, self.height)

    @timing
    def copyImage(self, tmp, path, w, h):
        old_size = w * h
        newI = []

        append = newI.append
        index = iter(path)
        it = next(index)
        last = path[-1]
        for i in range(last):
            if it == i:
                it = next(index)
            else:
                append(tmp[i])

        for i in range(last + 1, old_size):  # copie la derniere ligne
            append(tmp[i])

        return newI




def debug_path(w, h, path, img):
    """fonction qui permet de visualiser le chemin qui sera supprimer"""
    ni = Image.new("RGB",(w,h))

    for p in path:
        img[p] = (255,0,0)
    ni.putdata(img)
    ni.show()


