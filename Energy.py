import Utils
import math
from PIL import Image
import logging

class Energy:

    def __init__(self):
        self.width = 0
        self.height = 0
        self.img = None
        self.intensity = []
        self.energy_tab = []

    def calc_intensity(self):
        """calcul l intensite des pixel, la formule peut etre changer je pense"""
        logging.info("Processing intensity ...")
        self.intensity = [i for i in range(self.height*self.width)]
        for j in range(0, self.height):
            for i in range(0, (self.width)*3, 3):
                v = max(self.img[j*(self.width*3)+i], self.img[j*(self.width*3)+(i+1)], self.img[j*(self.width*3)+(i+2)])
                self.intensity[j*self.width + math.floor(i/3)] = v
        logging.info("Done.")

    def update_values(self, width, height, img):
        self.width = width
        self.height = height
        self.img = img
        self.energy_tab = []
        self.calc_intensity()

    def gradientX(self, i, j):
        """fonction annexe pour le calcul des graadient en X"""
        if (i <= 0 or j <= 0 or i >= self.width-1 or j >= self.height-1):
            return 255
        return self.intensity[(j-1)*self.width + (i-1)] + 2*self.intensity[(j)*self.width + (i-1)] + self.intensity[(j+1)*self.width + (i-1)] - self.intensity[(j-1)*self.width + (i+1)] - 2*self.intensity[(j)*self.width + (i+1)] -self.intensity[(j+1)*self.width + (i+1)]

    def gradientY(self, i, j):
        """fonction annexe pour le calcul des graadient en X"""
        if(i <=0 or j<=0 or i>=self.width-1 or j>=self.height-1):
            return 255
        return self.intensity[(j-1)*self.width + (i-1)] + 2*self.intensity[(j-1)*self.width + (i)] + self.intensity[(j-1)*self.width + (i+1)] - self.intensity[(j+1)*self.width + (i-1)] - 2*self.intensity[(j+1)*self.width + (i)] -self.intensity[(j+1)*self.width + (i+1)]

    def calc_energy(self):
        """calcul l energie de chaque pixel"""
        logging.info("Processing energy ...")
        self.energy_tab = [i for i in range(self.height*self.width)]
        for j in range(0, self.height):
            for i in range(0, self.width):
                r = math.floor(math.sqrt(pow(self.gradientY(i,j),2) + pow(self.gradientX(i,j),2)))
                self.energy_tab[j*self.width + i] = r
        logging.info("Done.")

    def chemin_less_energy(self):
        """calcul le chemin d energie la plus faible"""
        logging.info("Processing path of minimum energy ...")
        self.cost = [i for i in range(self.width*self.height)]
        for i in range(self.width):
            self.cost[i] = self.energy_tab[i]

        for j in range(0,self.height-2):
            for i in range(0,self.width):
                if(i == self.width):
                    self.cost[j*self.width + i] = self.cost[j*self.width + i] + min(self.cost[(j+1)*self.width + i-1], self.cost[(j+1)*self.width + i])
                elif (i == 0):
                    self.cost[j * self.width + i] = self.cost[j*self.width + i] + min(self.cost[(j + 1) * self.width + i], self.cost[(j + 1) * self.width + (i + 1)])
                else:
                    self.cost[j * self.width + i] = self.cost[j*self.width + i] + min(self.cost[(j + 1) * self.width + i-1], self.cost[(j+1) * self.width + i] ,self.cost[(j + 1) * self.width + (i + 1)])
        logging.info("Done.")

    def min_neighbour(self,cx,cy):
        x,y = cx,cy
        cv = self.cost[cy*self.width + cx]
        for i in range(-1,2):
            if cv >= self.cost[(cy-1)*self.width + i]:
                x,y = cx+i,cy-1
                cv = self.cost[(cy-1)*self.width + i]
        return cv,x,y


    def find_path(self):
        """recup le chemin en remontant le tableau cost """
        logging.info("Get the path from cost ...")
        self.path = [i for i in range(self.height)]
        current = math.inf
        k=1
        for i in range(self.width):
            if current > self.cost[self.width*(self.height-1) + i]:
                cx,cy = (i,(self.height))
        self.path[0] = cx,cy
        for i in range(self.height-1,0,-1):
            cv,cx,cy = self.min_neighbour(cx,i)
            self.path[k] = cx,cy
            k +=1
        logging.info("Path found")
        print("Minimum path is" , self.path) #je sais pas comment afficher le log avec le path en argument alors je print

    def shrink_image(self, widget):
        self.chemin_less_energy()
        self.find_path()