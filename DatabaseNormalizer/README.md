# DatabaseNormalizer

Sous-projet destiné à convertir des `.dat` en `.csv` puis à en extraire les données
en vue de les intégrer en base.

## Chargement des données CSV en base

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

### Conception

Le projet est en **Python 3.6+** et sa structure basée sur celle du très célèbre micro framework [Flask](https://github.com/pallets/flask).


### Outils

Le projet présente deux outils majeurs:

-   Convertisseur `.dat` - -> `.csv`

-   Lecteur de `.csv`


### Conversion de fichiers `dat`

Lire un fichier unique:

```python
    # Creating the normalizer object for .dat files
    normalizer = Normalizer(
        to_normalize_ext=Dat.ext,
        separator=Dat.separator
    )

    # Normalizing the given .dat file
    normalizer.convert_to_csv(
        dat_path='../static/data/dat_files/airports.dat',
    )
```

Lire un dossier contenant les `.dat`:

```python
    # Creating the normalizer object for .dat files
    normalizer = Normalizer(
        to_normalize_ext=Dat.ext,
        separator=Dat.separator,
    )

    # Normalizing each .dat files in the data folder
    normalizer.convert_to_csv_from_folder(
        dat_folder='../static/data/dat_files'
    )
```

### Lire le contenu d'un fichier `.csv`

```python
    reader = Reader('../static/data/csv_files/airlines.csv')
    content = reader.read_content(skip_header=True)

    print(f'The file contains {reader.rows} rows and {reader.columns} columns')
```
