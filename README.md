*** Installations requises ***
sudo apt install python3-tk
sudo apt install python3-numpy
sudo apt-get install python3-pil.imagetk

*** Divers *** 
- Interface graphique GTK+3
- Logger pour débeugg
- GUI.py -> gestion de l'interface graphique
- Utils.py -> fonction utilitaires, constantes, etc
- Main.py -> Appel de l'interface
- /c_files -> Contient des fichiers c pour accélrer le code
- Ajout de décorateur time : Passage de 5s pour calculer les énergies( pas les chemins) à 0.3s
- COmpiler les fichiers fichier python : - gcc -shared -Wl -lm,-soname,gradient -o gradient.so -fPIC gradient.c
                                         - gcc -shared -Wl,-soname,lessEnergyPath -o lessEnergyPath.so -fPIC lessEnergyPath.c

