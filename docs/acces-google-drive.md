# Donner à GitHub l'accès au dossier Google Drive

Chaque nuit, l'action « Synchroniser les contenus depuis Google Drive » va chercher le dernier paquet déposé par l'Atelier, le décompresse dans `contenus/` et enregistre une nouvelle version du dépôt. Pour lire le dossier Drive, elle a besoin d'une clé Google. C'est à faire une seule fois.

## 1. Créer un compte de service Google

1. Ouvrir la console Google Cloud (console.cloud.google.com) et créer un projet, par exemple « visites-etat-sync ».
2. Dans « API et services », activer l'API Google Drive.
3. Dans « IAM et administration », puis « Comptes de service », créer un compte de service. Aucun rôle n'est nécessaire.
4. Dans l'onglet « Clés » du compte, ajouter une clé au format JSON. Le fichier se télécharge.

Le compte de service a une adresse du type `visites-etat-sync@visites-etat-sync.iam.gserviceaccount.com`.

## 2. Partager le dossier Drive avec ce compte

Dans Google Drive, partager le dossier « Visites d'État · version digitale · paquets » avec l'adresse du compte de service, en lecture seule.

## 3. Ranger la clé dans GitHub

Dans le dépôt, menu Settings, puis Secrets and variables, puis Actions :

- onglet Secrets : créer `GDRIVE_SA_JSON` et y coller tout le contenu du fichier JSON ;
- onglet Variables (facultatif) : créer `GDRIVE_FOLDER_ID` si le dossier change. Par défaut, l'action utilise `1Dwssd7c9EMObZ0ZM6ZNk5ghx_1FDOuYX`.

Supprimer ensuite le fichier JSON de l'ordinateur : la clé ne doit vivre que dans GitHub.

## 4. Vérifier

Onglet Actions, « Synchroniser les contenus depuis Google Drive », bouton « Run workflow ». Si un paquet plus récent que celui du dépôt est dans le dossier, un nouveau commit apparaît, avec le résumé des changements en message. Sinon, l'action s'arrête sans rien écrire.
