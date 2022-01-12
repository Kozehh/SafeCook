# Installation d'un environnement pour entrainer un modèle de détection d'objets

# Requis
- [Anaconda on Windows](https://docs.anaconda.com/anaconda/install/windows/)
- [Anaconda on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart)
- Pip
- Python 2.7+
- git

# Installation
``` bash
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```
Voir quelle commande à utiliser pour installer [Pytorch](https://pytorch.org)

# Utilisation
1. Dans le dossier yolov5/data/, créer un fichier yaml (ex: safecook.yaml) et créer un nouveau dossier (ex: safecook).
2. Dans le dossier, on veut mettre tous les images et les labels obtenus pour entrainer le modèle. Voici le format à suivre pour que YOLOv5 puisse y accéder :
- yolov5/data/safecook/train/images -> Pour tous les images d'entrainement
- yolov5/data/safecook/train/labels -> Pour tous les labels associés aux images d'entrainement
- yolov5/data/safecook/valid/images -> Pour tous les images de validation
- yolov5/data/safecook/valid/labels -> Pour tous les labels associés aux images de validation
- yolov5/data/safecook/test/images -> Pour tous les images de test
- yolov5/data/safecook/test/labels -> Pour tous les labels associés aux images de test

**Note**: Le type de fichier pour les labels accepté par YOLOv5 est de type .txt

3. Pour le fichier yaml créé précédement, il faut spécifier l'emplacement des images d'entrainement et de validation ainsi que les différentes classes associés aux images.

**Exemple:**
``` yaml
train: data/safecook/train/images
val : data/safecook/valid/images

nc: 4 
names: ['Frying pan', 'Human hand', 'Gas stove', 'Spoon']
```
4. Choisir et modifier en conséquences du nombre de classes le fichier de configuration YOLOv5.
Selon le modèle choisi (voir différences dans le tableau ci-dessous), ouvrir son fichier de configuration yaml se trouvant au chemin yolov5/models.
Modifier le nombre de classes (nc) pour l'ajuster au nombre de classes que vous allez entrainer.


## Pretrained Checkpoints

| Model | size | AP<sup>val</sup> | AP<sup>test</sup> | AP<sub>50</sub> | Speed<sub>V100</sub> | FPS<sub>V100</sub> || params | GFLOPS |
|---------- |------ |------ |------ |------ | -------- | ------| ------ |------  |  :------: |
| [YOLOv5s](https://github.com/ultralytics/yolov5/releases)    |640 |36.8     |36.8     |55.6     |**2.2ms** |**455** ||7.3M   |17.0
| [YOLOv5m](https://github.com/ultralytics/yolov5/releases)    |640 |44.5     |44.5     |63.1     |2.9ms     |345     ||21.4M  |51.3
| [YOLOv5l](https://github.com/ultralytics/yolov5/releases)    |640 |48.1     |48.1     |66.4     |3.8ms     |264     ||47.0M  |115.4
| [YOLOv5x](https://github.com/ultralytics/yolov5/releases)    |640 |**50.1** |**50.1** |**68.7** |6.0ms     |167     ||87.7M  |218.8
| | | | | | | || |
| [YOLOv5x](https://github.com/ultralytics/yolov5/releases) + TTA |832 |**51.9** |**51.9** |**69.6** |24.9ms |40      ||87.7M  |1005.3

**5. Entrainement du modèle**
Liste des hyperparamètres :
- img : define input image size
- batch : determine batch size
- epochs : define the number of training epochs
- data : set the path to our YAML file
- cfg : specify our model configuration
- weights : specify a custom path to our weights file
- name : result names
- nosave : only save the final checkpoint
- cache : cache images for faster training

Exemple de commande pour lancer l'entrainement: *(Commande à exécuter dans un terminal Anaconda)*
``` bash
python train.py --batch_size 16 --data data/safecook.yaml --cfg models/yolov5x.yaml --weights''
```

Exemple de commande pour tester le fichier de poids:
```bash
python detect --source data/safecook/test/images --weights best.pt --conf 0.3
```

**Pour plus d'informations et d'aide pour entrainer un modèle personnalisé avec YOLOv5, voici quelques références :**
- [YOLOv5](https://github.com/ultralytics/yolov5)
- [YOLOv5_Tutorial](https://michaelohanu.medium.com/yolov5-tutorial-75207a19a3aa)
- [YOLOv5_Custom_Model](https://medium.com/analytics-vidhya/training-a-custom-object-detection-model-with-yolo-v5-aa9974c07088)

