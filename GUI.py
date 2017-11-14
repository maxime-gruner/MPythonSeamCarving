import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import logging
import Utils

DEFAULT_SPACING = 6

class MyGUI(Gtk.Window):

    def __init__(self, parent):
        """ Creating the Interface. Parent in the main function"""
        Gtk.Window.__init__(self, title="SeamCarving")
        # Data
        self.parent = parent
        self.img_width = 0
        self.img_height = 0
        self.img = None

        # Widgets
        self.frame = Gtk.Frame(label="Image")
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=DEFAULT_SPACING)
        self.shrink_button = Gtk.Button(label="Rétrécir")
        self.shrink_button.connect("clicked", self.parent.energy.shrink_image)
        self.open_button = Gtk.Button(label="Ouvrez une image")
        self.open_button.connect("clicked", self.loadImage)
        self.vbox.pack_start(self.open_button, expand=True, fill=True, padding=DEFAULT_SPACING)
        self.add(self.vbox)
        self.connect("delete-event", self.exit_program)
        self.show_all()
        Gtk.main()

    def loadImage(self, widget):
        logging.info("Creating dialog to choose an image to open")
        dialog = Gtk.FileChooserDialog("Ouvrez une image", self,
                                                       Gtk.FileChooserAction.OPEN,
                                                       ("Annuler", Gtk.ResponseType.CANCEL,
                                                        "Ouvrir", Gtk.ResponseType.OK))
        dialog.set_current_folder(Utils.IMAGE_PATH)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.parent.image_name = dialog.get_filename()
            logging.info("opening the image " + self.parent.image_name)
            dialog.destroy()
            self.loadFrame(self.parent.image_name)
        else:
            logging.info("Cancelling the opening file Dialog")
            dialog.destroy()

    def loadFrame(self, name):
        logging.info("creating Frame")
        self.img = Gtk.Image.new_from_file(name)
        self.open_button.set_label("Ouvrir une autre image ")
        self.vbox.pack_start(self.shrink_button, expand=True, fill=False, padding=DEFAULT_SPACING)
        self.frame.add(self.img)
        self.vbox.pack_end(self.frame, expand=True, fill=False, padding=DEFAULT_SPACING)
        self.vbox.show_all()
        self.parent.energy.update_values(self.img.get_pixbuf().get_width(),
                                         self.img.get_pixbuf().get_height(), self.img.get_pixbuf().get_pixels())

        self.parent.energy.calc_energy()

    def exit_program(self,a1,a2):
        logging.info("closing the GUI")
        logging.info("****Closing session*****")
        Gtk.main_quit()



