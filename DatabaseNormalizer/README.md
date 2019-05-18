# DatabaseNormalizer

Sous-projet destiné à convertir des `.dat` en `.csv` puis à en extraire les données
en vue de les intégrer en base.

## Chargement des données CSV en base

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

### Conception

Le projet est en **Python 3.6+** et sa structure basée sur celle du très célèbre micro framework
[Flask](https://github.com/pallets/flask).

### Tests

Les tests unitaires associés au projet sont disponibles dans le dossier `tests/`.
Pour leur execution, executer: `python -m unittest discover --start-directory tests`:

```powershell
PS D:\_Programmes\project-grpa2\DatabaseNormalizer> python -m unittest discover --start-directory tests
....................
----------------------------------------------------------------------
Ran 20 tests in 0.017s

OK
PS D:\_Programmes\project-grpa2\DatabaseNormalizer>
```

### Outils

Le projet présente trois outils majeurs:

- Outil csv:
  - Convertisseur `.dat` vers `.csv`
  - Lecteur de `.csv`
- Outil de chargement de données
- Couche communicante entre base de données et données en mémoires

### Outil csv

#### Conversion de fichiers `dat`

Lire un fichier unique:

```python
my_dat_source = 'some_awesome_records.dat'

# Creating the normalizer object for .dat files
normalizer = Normalizer(
    to_normalize_ext=Dat.ext,
    separator=Dat.separator
)

# Normalizing the given .dat file
normalizer.convert_to_csv(
    dat_path=my_dat_source,
)
```

Lire un dossier contenant les `.dat`:

```python
my_dat_sources = 'some_awesome_records/'

# Creating the normalizer object for .dat files
normalizer = Normalizer(
    to_normalize_ext=Dat.ext,
    separator=Dat.separator,
)

# Normalizing each .dat files in the data folder
normalizer.convert_to_csv_from_folder(
    dat_folder=my_dat_sources
)
```

#### Lire le contenu d'un fichier `.csv`

Depuis un fichier spécifique, lire le csv qu'il contient est facile:

```python
my_csv_source = 'some_awesome_records.csv'

reader = Reader(my_csv_source)
content = reader.read_content(skip_header=True)

print(f'The file contains {reader.rows} rows and {reader.columns} columns')
```

### Chargement des données

Pour charger les données en mémoire la procédure est la suivante:

```python
# création d'un objet `Loader` qui chargera nos données
loader = Loader()

# chargement de toutes les données brutes dans les fichiers `.csv` de référence
loader.load_all_raw()

# chargement de données externes (superficie et population des pays, etc.)
loader.load_external(smooth=True)
```

A noter:

- la personnalisation des sources est facilement possible en modifiant
  les valeurs associées dans `data_loader/utils/utils.py`
- il est possible de charger uniquement certaines tables à l'aide des
  méthodes associées
- l'utilisation de `smooth` défini le comportement en cas d'erreur, mettre
  cette valeur à `True` passera les erreurs sous silence
- le chargement des données externes est fait à l'aide de multiples appels
  à différentes APIs et prends donc un temps plus que considérable au vu
  du nombre de données à remplir

### Communication données et base de donnée

**Actuellement, le SGBD utilisé est sqlite3** car la librairie associée est inclue
dans python3 nativement, et nous permets de générer au fur et à mesure les données
en mémoire. Une migration ou un pont vers Oracle est prévu prochainement.

Là encore, le chargement est très facile, rapide, et se base sur le `Loader` présenté
précédemment:

```python
loader = Loader()
# remplissage du loader ...

# création de l'objet de liaison avec sqlite3
dal = Dal()

# création des tables depuis le dossier de référence (voir le utils.py associé)
dal.create_tables()

# stockage de toutes les données en base d'après celles chargées par le `loader`
dal.write_from_loader(loader)

# extraction du contenu de la base dans un fichier
dal.dump_content(dest='i_want_my_sql_there.sql')
```
