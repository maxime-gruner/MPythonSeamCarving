Installations requises
-

pip3 install python3-tk

pip3 install Pillow

pip3 install opencv-python

Le Projet
-

- [x] Gestion de l'interface
    - [x] Au lancement une première fenêtre s'ouvre demandant à l'utilisateur d'ouvrir une image.
    - [x] La fenêtre qui s'ouvre une fois l'image chargée est la fenêtre principale, elle comporte :
        - [x] Un bouton pour ouvrir une nouvelle fenêtre permettant d'afficher et gérer manuellement les énergies.
        - [x] Un bouton pour appliquer la détection des visages, testable avec l'image `images/lenna.jpeg`
        - [x] Un champ permettant de rentrer un nombre. Ce nombre sera le nombre de seams supprimés ou ajoutés
        - [x] Un bouton pour chaque type de seam : Vertical(resp. horizontal) pour faire un rétrécissement vertical(resp. horizontal)
        - [x] Des RadiosButtons pour choisir la méthode de calcul des énergies, et la méthode de calcul des seams.
    -  [x] La fenêtre d'énergie permet à l'utilisateur de dessiner manuellement sur l'image.
        Il peut ainsi avec la première barre choisir l'instensité qu'il souhaite donner aux pixels qu'il va sélectionner,
        et avec la deuxième, il peut choisir la taille du pinceau. Il confirme ensuite pour sauvegarder le résultat, ce qui
        permet de préserver des zones, ou au contraire d'en supprimer.
- [x] Calcul de l'énergie
    - [x] Méthode des gradients, codé en C dans le fichier `c_files/gradient.c`.
     Les résultats sont visibles en appuyant sur le bouton "ouvrir l'image d'énergie", après avoir ouvert une image.
    - [x] Méthode de Histogramme de gradient orienté (HOG) : codé en C dans le fichier 'c_files/gradient.c' .
    La méthode consiste à calculer les gradients et leurs angles sur 180 degré. On parcourt l'image avec une fenetre de 11x11 autour de chaque pixel. Dans cette fenetre, on construit un histogramme de 8 valeurs representant les degrés de 0 a 180. Chaque gradient de pixel dans cette fenetre va voter pour la valeur dont il est le plus proche. A la fin on divise le gradient par la valeur qui aura le plus de vote,
 	Cette technique donne au bord une plus grande energie, ce qui permet de les conserver


- [x] Calcul du(des) chemin(s) d'énergie minimale
    - [x] Méthode du SeamCarving(SC), qui retourne le chemin de plus faible énergie,
     codé en C, dans le fichier `c_files/less_energy_path.c`. Utilisation de la programmation dynamique,
      avec plusieurs tableau pour stocker la valeur minimale d'un pixel jusqu'au bas de l'image, ainsi que le pixel
      à suivre pour arriver à cette valeur minimale. Permet de retirer les seams une à une,
       la seam étant supprimée de l'image entre chaque calcul (fonction `reduce_image`).
    - [x] Methode du Non Cumulative Seam Carving (NCSC), inspiré de http://hpc.cs.tsinghua.edu.cn/research/cluster/papers_cwg/icpads14.pdf .
      Ici, on s'intéresse non pas au cumul des énergie des pixels inférieur pour décider du chemin à prendre, mais à la valeur
      des énergies des pixels inférieur. Cette méthode est codée en Python par la fonction `Energy.py :: getNCSCpath`.
      L'algorithme utilisé est le suivant : On cherche les seams qui commencent par un pixel de la première ligne. Quand
      2 seams se croisent, celle de plus haute valeur est abandonné, et on ne retient que la seam de plus faible énergie.
      Ainsi, parmi toutes les seams arrivant en bas de l'image, on sait que la seam est une minimum locale par la méthode.
      On est garanti de ne pas avoir de seams qui se croisent ou se chevauchent. On peut alors calculer la seam minimale,
      et supprimer toutes les seams dont la valeur du chemin d'énergie est inférieure à un pourcentage de la seam minimale donnée.
      C'est ce qui permet de pouvoir supprimé plusieurs seams d'un seul coup, et de diminuer drastiquement le temps d'exécution
      du programme.
      
      Metaphore pour comprendre la méthode NCSC:
      Une seam est comme un serpent du jeu Snake: elle commence de taille 1 pixel, tout en haut de l'image. La valeur d'une seam est la somme de toutes
      les énergies des pixels par lesquelles elle est déjà passé. À chaque étape, toutes les seams descendent vers le pixel d'énergie minimal
      parmi les 3 en dessous. Si 2 tête de seams arrivent sur un même pixel, celle qui avait la valeur minimal est conservée, et continue son chemin,
      tandis que l'autre est abandonnée. Ainsi, en bas de l'image, il ne restera que des seams minimales locales.
      On trouve ensuite la seam de valeur minimum parmi elles, et on la supprime, ainsi que toutes les seams dont les valeurs
      sont proches de la seam minimale.

- [x] Detection de visage: codé via openCV dans 'Energy.py'
openCV permet la reconnaissance d'un visage a l'aide d'un classifier  'haarcascade_frontalface_default.xml' situé dans le répertoire du projet. Ce fichier était donné sur le site d'openCV. La fonction renvoie alors un carré autour du visage si celui-ci est detecté. Ensuite on met l'energie de tous les pixel a l'interieur à 255 afin de preserver les visages du seamcarving. On peut visualiser cela en affichant l'image d'energie

Exemples pour Illustrer les fonctionnalités
-

Image: les 2 séries d'images suivantes ont été réduite de 100 seams verticales.
à gauche, avec la méthode du SeamCarving, à Droite avec NCSC:
![alt text](img_for_readme/pont_diff.png)
On remarque pour l'image du pont une amélioration avec la méthode non-cumulative, car elle permet de mieux détecter les contours

![alt text](img_for_readme/loutres_diff.png)
La différence est légère, mais les loutres de la méthode NCSC ont été rétrécie, contrairement à celle de la méthode du cumul d'énergie

Ci-dessous, nous avons l'exemple de la détection de visage, avec la méthode SC.
à gauche, sans détection, à doite, avec détection:
![alt text](img_for_readme/lenna_diff.png)

Ci-dessous, image du pont agrandie de 200pixels verticalement. A gauche, sans utiliser le pinceau sur le pont,
à droite, en utilisant la palette sur le pont:
![alt text](img_for_readme/pont_ajout.png)
