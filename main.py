import GUI
import Utils
import logging


class Main:
    def __init__(self):
        Utils.config_log()
        logging.info("Creating the GUI")
        self.gui = GUI.MyGUI(self)


Main()
