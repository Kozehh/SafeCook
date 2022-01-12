# Création d'un jeu de données d'images personnalisées pour YOLO
Afin d'entrainer un modèle pour la détection d'objets personnalisés, nous avons besoins d'un bon jeu de données d'images des objets et de les identifier en dessinant un encadré et en les étiquetant du nom de leur classe d'objet.

Pour construire ce jeu de données d'images personnalisées, nous utilisons un outil pour aller télécharger facilement des images de l'objet de notre choix sur Google images et un autre outil pour dessiner un encadré et étiqueter l'objet et qui nous retourne un fichier contenant des informations pertinentes pour l'algorithme de détection d'objet YOLO.

# Outils

## Anaconda
[On Windows](https://docs.anaconda.com/anaconda/install/windows/)

[On Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart)

## image_scrapper
[Github](https://github.com/Kozehh/image_scrapper.git)

## labelImg
[Github](https://github.com/tzutalin/labelImg)

# Utilisation image_scrapper
- Créer un dossier et naviguer à l'intérieur
- Cloner le [projet](https://github.com/Kozehh/image_scrapper.git) qui permet de télécharger des images sur internet.
- Installation des dépendances pour Download-Google-Images
```bash
cd image_scrapper
pip install -r requirements.txt
```
- Exécuter une commande
```bash
python download_images.py [URL]
```

# Utilisation labelImg
- Cloner [labelImg](https://github.com/tzutalin/labelImg).
- Pour ouvrir labelImg, il faut ouvrir un prompt Anaconda et naviguer jusqu'au dossier de base de labelImg.
- Exécuter la commande suivante pour ouvrir labelImg
```bash
python labelImg.py [IMAGE_PATH]
```
où IMAGE_PATH est le chemin vers le dossier contenant les images à étiqueter.
- Change le mode PascalVOC pour qu'on utilise le format YOLO

**Processus d'étiquetage des images**
- ctrl + w : pour commencer l'utilisation du cadrage
- Quand le cadrage est fait, il faut donner le nom respectif à la classe
- ctrl + s : pour sauvegarder l'image
- Cliquer sur le bouton "next" pour passer à la prochaine image et refaire le processus

**Pour plus d'informations sur l'utilisation du logiciel labelImg, veuillez vous référer au projet [Github](https://github.com/tzutalin/labelImg)**
