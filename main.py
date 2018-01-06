import GUI
import Utils
import logging
import tkinter as tk
from Energy import Energy


class Main:
    def __init__(self):
        Utils.config_log()
        logging.info("Creating the GUI")
        root = tk.Tk()
        self.gui = GUI.MyGUI(self, root)
        root.mainloop()

Main()


