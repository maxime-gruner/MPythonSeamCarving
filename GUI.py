import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import logging
import Utils


class MyGUI(Gtk.Window):

    def __init__(self, parent):
        """ Creating the Interface. Parent in the main function"""
        Gtk.Window.__init__(self, title="SeamCarving")
        self.parent = parent
        self.frame = Gtk.Frame(label="Image")
        self.box = Gtk.Box()
        self.button = Gtk.Button(label="Ouvrez une image")
        self.button.connect("clicked", self.loadImage)
        self.box.add(self.button)
        self.add(self.box)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        Gtk.main()

    def loadImage(self, widget):
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
        img = Gtk.Image.new_from_file(name)
        self.frame.add(img)
        self.box.add(self.frame)
        self.show_all()



