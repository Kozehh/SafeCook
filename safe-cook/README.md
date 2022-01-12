# Safe Cook

- [Information generale](#information-generale)
    - [Outils](#outils)
- [Installation et exécution](#installation-et-exécution)
    - [RaspberryPi](#raspberrypi)
    - [Object Detection Service](#object-detection-service)
    - [Information Processing Service](#information-processing-service)
    - [Web monitoring](#web-monitoring)
- [Utilisation](#utilisation)
        


## Information generale

Safe Cook est un système de vision par ordinateur qui a comme but d'être intégrée dans la cuisine intelligente du laboratoire DOMUS.

L'architecture du système est du type client-serveur.
* Les clients sont des webcams qui sont connectées à des Raspberry Pi et capturent des images vidéo.
* Le serveur est un ordinateur plus puissant qui reçoit les images vidéos et qui est capable de rouler un programme de détection d'objet rapidement.

Nous voulons que le serveur puisse faire de la détection d'objet en temps réel et qu'il offre une interface pour observer à distance le flux vidéo avec la détection d'objet en temps réel.

Nous allons utiliser la librairie ImageZMQ qui offre des fonctionnalités pour résoudre les problèmes de diffusion de flux vidéo en temps réel. Elle est très facile d'usage, fonctionne bien avec OpenCV et est basé sur le protocole ZMQ qui est un protocole de haute performance dans le passage de messages asynchrones.

### Outils

**Langages**
- Python 3.7
- Javascript

**Librairies/Frameworks**
- OpenCV
- Pytorch
- Flask
- YOLO

**Logiciels**
- Git
- GitLab
- labelImg
- image_scrapper

**Protocoles**
- ImageZMQ
- ZMQ
- SocketIO

**Matériel**
- Raspberry Pi
- Webcam

## Installation et exécution

### RaspberryPi
---

**Dépendances**

Exécuter les commandes suivantes dans un terminal du raspberry pi pour installer les dépendances
```bash
pip install opencv-contrib-python==4.1.0.25
pip install imagezmq
pip install imutils
git clone https://depot.domus.usherbrooke.ca/projet_etudiant/safe-cook.git
```

**Exécution**

Pour lancer l'application client sur le Raspberry Pi qui envoit les images du flux vidéo, exécuter dans le dossier Code:
```bash
python rpi_client.py -s <server_ip_address>
```
*server_ip_address : l'adresse ip où roule le service 'object_detection'*

### Object Detection Service
---
**Dépendances**

- Installer les dépendances en exécutant la commande dans le dossier racine du projet
```bash
pip install -r requirements.txt
```
- Ouvrir le port tcp:5555 pour ouvrir la connexion au protocole ZMQ

**Exécution**

```bash
python main.py -w <adresse_ip_serveur_debug> -o <weight_file> -c <cfg_file> -n <classes_name_file> -i <information_processing_service_ip>
```
**Note:** Pour l'instant, le service utilise des fichiers YOLOv4 pour le modèle entrainé (.weights, .cfg et obj.names). Notre façon trouvé pour entrainer facilement un modèle utilise YOLOv5 et le modèle résultant est seulement un fichier .pt (fichier de poids). **Alors**, il faudrait trouver une technique pour convertir le modèle résultant (.pt) à un format pour YOLOv4 ou trouver une façon d'utiliser OpenCV pour qu'il puisse utiliser un modèle YOLOv5 (.pt).

### Information Processing Service
---
**Dépendances**

- Python 3.7
- ZMQ
- numpy
```bash
pip install numpy
pip install zmq
```

**Exécution**

Pour lancer le service de traitement d'information, naviguer dans le dossier safe-cook/Code/information_processing/ et exécuter :
```bash
python main.py -o <path_to_obj.names>
```
*path_to_obj.names : fichier contenant tous les noms des classes du modèle*

### Web Monitoring
---
**Dépendances**

- Installer les dépendances en exécutant la commande dans le dossier racine du projet
```bash
pip install -r requirements.txt
```

**Exécution**

Pour lancer l'application de débbugage, naviguer dans le dossier safe-cook/Code/web_debugging et exécuter :
```bash
python main.py
```
**Note:** On peut spécifier l'adresse ip et le port que la page web s'exécute avec les arguments
*-i: ip address*
*-p: port*
Sinon, la page web roule sur http://localhost:5001

## Utilisation
Le système a présentement des problèmes de gestion des connexions entre services.

Ainsi, une des façons de faire qui fonctionne est de partir les 3 services (peu importe l'ordre) et d'exécuter le client sur le Raspberry Pi par la suite.


**Pour plus d'information sur les différents services, veuillez voir les différents fichiers de documentation qui se trouve dans le dossier du projet safe-cook/Documentation**
