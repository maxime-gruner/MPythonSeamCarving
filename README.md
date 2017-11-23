*** Installations requises ***
    sudo apt-get install python3-gi
    sudo pacman -S python-gobject (celle la je l ai pas faites, mais je suis passer par les module de pycharm pour install gobject )


*** Divers *** 
- Interface graphique GTK+3
- Logger pour débeugg
- GUI.py -> gestion de l'interface graphique
- Utils.py -> fonction utilitaires, constantes, etc
- Main.py -> Appel de l'interface
- /c_files -> Contient des fichiers c pour accélrer le code
- Ajout de décorateur time : Passage de 5s pour calculer les énergies( pas les chemins) à 0.3s
- COmpiler un fichier python : gcc -shared -Wl,-soname,gradient -o gradient.so -fPIC gradient.c^C

