# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from Energy import Energy
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

        # Widgets
        self.frame = tk.Frame(master, height=32, width=32)
        self.frame.pack()
        self.spin = tk.Spinbox(master, from_=1, to=100)
        self.shrink_button = tk.Button(self.frame, text="Rétrécir",
                                       command=lambda : self.energy.shrink_image(int(self.spin.get())))
        self.open_button = tk.Button(self.frame, text="Ouvrez une image", command=self.loadImage)
        self.open_button.pack()


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
            self.spin.pack()
            self.img = Image.open(self.image_name)
            img = ImageTk.PhotoImage(self.img)
            self.label = tk.Label(self.master, image=img)
            self.label.pack()
            self.label.image = img #obligatoire sinon tkinter bug

            self.img_width, self.img_height = self.img.size
            self.energy.update_values(self.img_width,
                                      self.img_height,
                                      image=self.img)
            self.loadFrame()
            self.label.bind("<Configure>", self.onResize)

    def updateImage(self, data, w, h):
        self.img = Image.new('RGB',(w,h))
        self.img.putdata(data)
        img = ImageTk.PhotoImage(self.img)
        self.label.configure(image=img)
        self.label.image = img #obligatoire
        self.label.pack()

        self.img_width,self.img_height = self.img.size
        self.loadFrame()



    def loadFrame(self):
        logging.info("creating Frame")
        self.open_button.pack_forget()
        self.shrink_button.pack()

    def exit_program(self,a1,a2):
        logging.info("closing the GUI")
        logging.info("****Closing session*****")
        self.master.main_quit()

    def onResize(self,event):

        newW = event.width
        oldW = self.img_width
        if(oldW-newW > 0):
            self.img_width = newW
            self.energy.shrink_image(oldW - newW)

