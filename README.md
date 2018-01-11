Installations requises
-

pip3 install python3-tk

pip3 install Pillow

pip3 install opencv-python

Le Projet
-

- [x] Gestion de l'interface
    - [x] Au lancement une première fenêtre s'ouvre demandant à l'utilisateur d'ouvrir une image.
    - [x] La fenêtre qui s'ouvre une fois l'image chargée est la fenêtre principale : elle comporte :
        - [x] Un bouton pour ouvrir une nouvelle fenêtre permettant d'afficher et gérer manuellement les énergies.
        - [x] Un bouton pour appliquer la détection des visages, testable avec l'image `images/facetest.jpeg`
        - [x] Un champs permettant de rentrer un nombre. Ce nombre sera le nombre de seams supprimés
        - [x] Un bouton pour chaque type de seam : Vertical(resp horizontal) pour faire un rétrécissement vertical(resp horizontal)
        - [x] Des RadiosButtons permettant de choisir la méthode de calcul des énergies, et la méthode de calcul des seams.
    -  [x] Le fenêtre d'énergie permet à l'utilisateur de dessiner manuellement sur l'image.
        Il peut ainsi avec la première barre choisir l'instensité qu'il souhaite donner aux pixel qu'il va sélectionner,
        et avec la deuxième, il peut choisir la taille du pinceau. Il confirme ensuite pour sauvegarder le résultat, ce qui
        permet de préserver des zones, ou au contraire d'en supprimer
- [x] Calcul de l'énergie
    - [x] Méthode des gradients, codé en C dans le fichier `c_files/gradient.c`.
     Les résultats sont visibles en appuyant sur le bouton "ouvrir l'image d'énergie", après avoir ouvert une image.
    - [x] Méthode de Histogramme de gradient orienté (HOG) : codé en C dan le fichier 'c_files/gradient.c' .
    La méthode consiste à calculer les gradients et leurs angles sur 180 degré. On parcourt l'image avec une fenetre de 11x11 autour de chaque pixel. Dans cette fenetre, on construit un histogramme de 8 valeurs representant les degrés de 0 a 180. Chaque gradient de pixel dans cette fenetre va voter pour la valeur dont il est le plus proche. A la fin on divise le gradient par la valeur qui aura le plus de vote,
 	Cette technique donne au bord une plus grande energie, ce qui permet de les conserver


- [x] Calcul du(des) chemin(s) d'énergie minimale
    - [x] Méthode du SeamCarving(SC), qui retourne le chemin de plus faible énergie,
     codé en C, dans le fichier `c_files/less_energy_path.c`. Utilisation de la programmation dynamique,
      avec plusieurs tableau pour stocker la valeur minimale d'un pixel jusqu'au bas de l'image, ainsi que le pixel
      à suivre pour arriver à cette valeur minimale. Permet de retirer les seams une à une,
       la seam étant supprimée de l'image entre chaque calcul (fonction `reduce_image`).
    - [x] Methode du Non Cumulative Seam Carving, inspiré de http://hpc.cs.tsinghua.edu.cn/research/cluster/papers_cwg/icpads14.pdf.
      Ici, on s'intéresse non pas au cumul des énergie des pixels inférieur pour décider du chemin à prendre, mais de la valeur
      des énergies des pixels inférieur. Cette méthode est codée en Python par la fonction `Energy.py :: getNCSCpath`.
      L'algorithme utilisé est le suivant : On cherche les seams qui commencent par un pixel de la première ligne. Quand
      2 seams se croisent, celle de plus haute valeur est abandonné, et on ne retient que la seam de plus faible énergie.
      Ainsi, parmi toutes les seams arrivant en bas de l'image, on sait que la seam est une minimum locale par la méthode.
      On est garanti de ne pas avoir de seams qui se croisent ou se chevauchent. On peut alors calculer la seam minimale,
      et supprimer toutes les seams dont la valeur du chemin d'énergie est inférieure à un pourcentage de la seam minimale donnée.
      C'est ce qui permet de pouvoir supprimé plusieurs seams d'un seul coup, et de diminuer drastiquement le temps d'exécution
      du programme.

- [x] Detection de visage: codé via openCV dans 'c_files/Energy.py'
openCV permet la reconnaissance d'un visage a l'aide d'un classifier  'haarcascade_frontalface_default.xml' situé dans le répertoire du projet. Ce fichier était donné sur le site d'openCV. La fonction renvoie alors un carré autour du visage si celui-ci est detecté. Ensuite on met l'energie de tous les pixel a l'interieur à 255 afin de preserver les visages du seamcarving. On peut visualiser cela en affichant l'image d'energie

Exemple pour Illustrer les fonctionnalités
-

