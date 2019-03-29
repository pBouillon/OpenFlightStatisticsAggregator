# Projet S6

[![](https://img.shields.io/badge/Database%20Master-Alexandre%20Cesari-green.svg?logo=stackoverflow&longCache=true&style=popout&colorB=fc6d26&link=https://gitlab.telecomnancy.univ-lorraine.fr/ppii-2k19/project-grpa2&link=mailto:alexandre.cesari@telecomnancy.eu
)]()
[![](https://img.shields.io/badge/Git%20Master-Pierre%20Bouillon-green.svg?logo=gitlab&longCache=true&style=popout&colorB=fc6d26&link=https://gitlab.telecomnancy.univ-lorraine.fr/ppii-2k19/project-grpa2&link=mailto:pierre.bouillon@telecomnancy.eu
)]()

## Partie I: normalisateur et injecteur de données

### Installation

Se rendre dans le dossier du projet, et installer les dépendances:

```bash
~ $ cd DatabaseNormalizer
~/DatabaseNormalizer $ sudo make install
```

_Note_: permission `sudo` indispensables pour le téléchargement de la librairie
`pathlib2` depuis `pip3`.

### Tester le projet

Se rendre dans le dossier du projet, et lancer la directive de test:

```bash
~ $ cd DatabaseNormalizer
~/DatabaseNormalizer $ make test
```

_Note_: la directive de test va automatiquement explorer tous les sous dossiers
et fichiers de tests existants et les lancer à la suite.
