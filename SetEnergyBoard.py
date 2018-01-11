# -*- coding: utf-8 -*-

from tkinter import *
from PIL import ImageDraw, ImageTk


class SetEnergyBoard(Toplevel):
    '''Crée une fenêtre pour pouvoir changer les énergies des pixels manuellement.
        L'utilisateur trace sur l'image des energies les zones qu'il veut réduire ou augmenter'''
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 255

    def __init__(self, master, background,w ,h):
        Toplevel.__init__(self, master)
        self.draw = ImageDraw.Draw(background)
        self.bg = background
        self.master = master
        self.new_energy_tab = []
        self.tmp = ImageTk.PhotoImage(background)

        self.confirm = Button(self, text='confirmer', command=self.confirm)
        self.confirm.pack()

        self.cancel = Button(self, text='annuler', command=self.cancel)
        self.cancel.pack()

        self.choose_energy_button = Scale(self, from_=0, to=255, orient=HORIZONTAL)
        self.choose_energy_button.pack()

        self.choose_size_button = Scale(self, from_=1, to=100, orient=HORIZONTAL)
        self.choose_size_button.pack()

        frame = Frame(self)
        self.c = Canvas(frame, bg='white', width=w, height=h)
        self.c.create_image(0,0, image=self.tmp, anchor="nw")
        frame.pack()
        self.c.pack()

        self.setup()

    def confirm(self):
        self.new_energy_tab = list(self.bg.getdata())
        self.destroy()

    def cancel(self):
        self.destroy()

    def getTab(self):
        self.wait_window()
        return self.new_energy_tab


    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        decimal = self.choose_energy_button.get()
        hexa = str(hex(decimal))
        hexa = hexa[2:]
        paint_color = "#"+hexa+hexa+hexa

        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.draw.line([self.old_x,self.old_y, event.x, event.y], width=self.line_width, fill=paint_color)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None
