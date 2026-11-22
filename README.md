# Visites d'État · version digitale

Ce dépôt reçoit la matière de la version digitale des visites d'État : une expérience immersive par visite, traversée par le fil vermillon, en sept salles. La matière est préparée dans l'Atelier de l'ouvrage. Le design, les effets, le son, la vidéo et la mise en ligne se font ici, dans l'environnement du Chief Digital Publisher.

## D'où viennent les contenus

L'Atelier dépose chaque jour un paquet dans le dossier Google Drive « Visites d'État · version digitale · paquets ». Chaque nuit, une action GitHub récupère le paquet le plus récent et l'enregistre ici comme une nouvelle version. Le message de la version résume ce qui a changé ; le détail est dans le `CHANGELOG.md` de chaque visite.

Le dossier `contenus/` est donc écrit par l'automate. Ne pas le modifier à la main : la nuit suivante l'écraserait. Pour corriger un contenu, passer par l'Atelier.

La mise en place de l'accès à Drive est décrite dans [docs/acces-google-drive.md](docs/acces-google-drive.md).

## Ce que contient chaque visite

```
contenus/visite-19-maroc/
  manifest.json          la visite, sa phase, la version du paquet, l'état du livre (BAT)
  content/*.json         un fichier par type de contenu
  textes/                discours intégraux et textes de salle, en Markdown
  livre/                 le chapitre du livre (papier et livre numérique) et ses médias
  medias/                les fichiers d'origine
  credits-droits.csv     crédit et droits de chaque média
  CHANGELOG.md           ce qui a changé depuis le paquet précédent
```

Les types de contenu sont décrits dans [schema.json](schema.json) :

| Type | Salle | Contenu |
| --- | --- | --- |
| `salle` | toutes | titre, surtitre, introduction, narration du fil |
| `evenement` | Galerie du temps | la frise |
| `etape` | Itinéraire | jour, heure, lieu, coordonnées, programme officiel, résumé |
| `discours` | Chambre des mots | texte intégral, source, enregistrement, transcription horodatée |
| `passage` | Chambre des mots | extraits classés par thème |
| `accord` | Engagements | intitulé, instrument, signataires des deux pays, secteur, montant |
| `personne` | Galerie humaine | nom, fonction à la date de la visite, catégorie |
| `perspective` | Galerie humaine, Horizon | vitrines et perspectives |
| `media` | toutes | photo, vidéo, son, carte ; crédit, droits, texte alternatif |
| `verif` | aucune | journal des vérifications éditoriales |

## Deux règles à respecter

Chaque élément porte un `statut` : Prototype, En cours, Validé ou Écarté. Tout arrive, même ce qui n'est pas fini ; c'est ici qu'on choisit ce qu'on montre.

Chaque média porte `publiable`. Il vaut `false` tant que les droits ne sont pas réglés (accordés, payés ou libres). Un média non publiable peut servir aux maquettes internes. Il ne doit jamais être mis en ligne.

## Où en est le contenu

La visite 19 (Maroc) sert de pilote. Ses données viennent du prototype « Le Fil vermillon » : 7 salles, 20 événements de frise, 15 étapes, 2 discours intégraux et 46 passages par thème, 18 accords, 113 personnes, 80 photos et 24 vérifications. Elles sont en phase « Prototype » et seront consolidées après le BAT du livre. Les 80 photos n'ont pas encore de crédit : toutes sont non publiables.

Le premier paquet, déposé à la main le 22 novembre 2026, ne contient pas encore le chapitre du livre (`livre/`). Il arrivera avec le premier transfert automatique.
