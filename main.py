import GUI
import Utils
import logging
from Energy import Energy


class Main:
    def __init__(self):
        Utils.config_log()
        logging.info("Creating the GUI")
        self.energy = Energy()
        self.gui = GUI.MyGUI(self)


Main()
