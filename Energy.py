import Utils


class Energy:

    def __init__(self):
        self.width = 0
        self.height = 0
        self.pixels = None
        self.energy_tab = []

    def update_values(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels
        self.energy_tab = []


    def calc_energy(self):
        pass

    def shrink_image(self, widget):
        pass