# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from Energy import Energy
from SetEnergyBoard import SetEnergyBoard
import logging
import Utils

DEFAULT_SPACING = 6


class MyGUI:

    def __init__(self, parent, master):
        """ Creating the Interface. Parent in the main function"""
        self.master = master
        self.master.title("SeamCarving")
        # Data
        self.image_name = ""
        self.parent = parent
        self.img_width = 0
        self.img_height = 0
        self.img = None
        self.energy = Energy(self)
        self.nmode_energy = 2
        self.value_energy = [0,1]
        self.name_energy = ["Gradient", "HOG"]
        self.v_energy = tk.IntVar()

        # Widgets
        self.frame = tk.Frame(master, height=32, width=32)

        self.resize_panel = tk.Frame(self.master)
        self.other_panel = tk.Frame(self.master)
        self.radio_panel = tk.Frame(self.master)

        self.frame.pack()
        self.spin = tk.Spinbox(self.resize_panel, from_=1, to=100)
        self.shrink_vertical_button = tk.Button(self.resize_panel, text="Enlever seam horizontale",
                                                command= lambda : self.on_click(0))
        self.shrink_horizontal_button = tk.Button(self.resize_panel, text="Enlever seam verticale",
                                                  command=lambda : self.on_click(1))
        self.detection = tk.Button(self.other_panel,text = "Detection des visage",command = self.face_detection)
        self.open_energy_button = tk.Button(self.other_panel, text="Ouvrir l'image d'énergie", command=self.displayEnergy)
        self.open_button = tk.Button(self.frame, text="Ouvrez une image", command=self.loadImage)
        self.open_button.pack()

    def displayEnergy(self):
        '''Créer un pop-up permettant de changer manuellement les valeurs d'énergie'''
        tmp = Image.new('L', (self.img_width, self.img_height))
        tmp.putdata(self.energy.energy_tab)
        board = SetEnergyBoard(self.master, tmp, self.img_width, self.img_height).getTab()
        if board:
            self.energy.energy_tab = board

    def getFilenameChoosed(self):
        logging.info("Creating dialog to choose an image to open")
        filename = filedialog.askopenfilename(parent=self.master, title='Ouvrez une image', initialdir=Utils.IMAGE_PATH)
        if filename:
            logging.info("opening " + filename)
            return filename
        else:
            logging.info("Opening file cancelled")

    def loadImage(self):
        self.image_name = self.getFilenameChoosed()

        if not self.img:
            self.img = Image.open(self.image_name)

            img = ImageTk.PhotoImage(self.img)
            self.img_width, self.img_height = self.img.size
            self.label = tk.Label(self.master, image=img)
            self.label.image = img #obligatoire sinon tkinter bug

            self.energy.update_values(self.img_width,
                                      self.img_height,
                                      image=self.img)

            self.label.bind("<Configure>", self.onResize)

            self.detection.pack(side = tk.LEFT)
            self.open_energy_button.pack(side = tk.LEFT)
            self.loadFrame()


            for i in range(self.nmode_energy):
                b = tk.Radiobutton(self.radio_panel, variable=self.v_energy, text=self.name_energy[i],
                                   value=self.value_energy[i], command = self.click_Radio)
                b.pack(side = tk.LEFT)

            self.other_panel.pack()
            self.resize_panel.pack()
            self.radio_panel.pack()
            self.label.pack(side=tk.BOTTOM)

            self.v_energy.set(0)
            self.energy.energy_tab = self.energy.calc_energy(self.energy.imgBW)

    def updateImage(self, data, w, h):
        self.img = Image.new('RGB',(w,h))
        self.img.putdata(data)
        img = ImageTk.PhotoImage(self.img)
        self.label.configure(image=img)
        self.label.image = img #obligatoire
        self.img_width,self.img_height = self.img.size
        self.loadFrame()



    def loadFrame(self):
        logging.info("creating Frame")
        self.open_button.pack_forget()

        self.shrink_vertical_button.pack(side = tk.LEFT)
        self.shrink_horizontal_button.pack(side = tk.LEFT)
        self.spin.pack(side = tk.LEFT)

    def exit_program(self,a1,a2):
        logging.info("closing the GUI")
        logging.info("****Closing session*****")
        self.master.main_quit()

    def on_click(self, orientation):
        self.energy.shrink_image(int(self.spin.get()), orientation)


    def onResize(self,event):
        newW = event.width
        oldW = self.img_width
        newH = event.height
        oldH = self.img_height
        if oldW-newW > 0:
            self.img_width = newW
            self.energy.shrink_image(oldW - newW,1)
        if oldH - newH > 0:
            self.img_height = newH
            self.energy.shrink_image(oldH - newH, 0)

    def face_detection(self):
        self.energy.detection()

    def click_Radio(self):
        v = self.v_energy.get()
        if v == 0:
            self.energy.energy_tab = self.energy.calc_energy(self.energy.imgBW)
        elif v == 1:
            self.energy.energy_tab = self.energy.calc_energy_hog(self.energy.imgBW)
