# Projet S6

[![](https://img.shields.io/badge/Database%20Master-Alexandre%20Cesari-green.svg?logo=stackoverflow&longCache=true&style=popout&colorB=fc6d26&link=https://gitlab.telecomnancy.univ-lorraine.fr/ppii-2k19/project-grpa2&link=mailto:alexandre.cesari@telecomnancy.eu
)]()
[![](https://img.shields.io/badge/Git%20Master-Pierre%20Bouillon-green.svg?logo=gitlab&longCache=true&style=popout&colorB=fc6d26&link=https://gitlab.telecomnancy.univ-lorraine.fr/ppii-2k19/project-grpa2&link=mailto:pierre.bouillon@telecomnancy.eu
)]()

## Partie I: normalisateur et injecteur de données

### Installation

Se rendre dans le dossier du projet, et installer les dépendances:

```bash
~$ cd DatabaseNormalizer
~/DatabaseNormalizer$ sudo make install
```

_Note_: permission `sudo` indispensable pour le téléchargement de la librairie
`pathlib2` depuis `pip3`.

### Tester le projet

Se rendre dans le dossier du projet, et lancer la directive de test:

```bash
~$ cd DatabaseNormalizer
~/DatabaseNormalizer$ make test
```

_Note_: la directive de test va automatiquement explorer tous les sous dossiers
et fichiers de tests existants et les lancer à la suite.

### Requetes de la base de données - Partie 1

_Note_: pour requeter la base de données, un simple script Python peut-être utilisé:

```Python
import sqlite3


def perform_request(country_name: str = 'Ireland'):
    conn = sqlite3.connect('ppii.db')
    curs = conn.cursor()

    sql = f'select * from airport, city, country ' \
          + 'where airport.id_city = city.id ' \
          + 'and city.id_country = country.id ' \
          + 'and country.name like "{country_name}"'

    curs.execute(sql)

    print('Liste des aéroports dans un pays donné:')
    for line in curs.fetchall():
        print(line)

    conn.close()


if __name__ == '__main__':
    perform_request()
```

#### Requête 1

But: _Liste des aéroports dans un pays donné_

Requête:
```sql
SELECT
    *
FROM
    airport,
    country,
    city
WHERE
    airport.id_city = city.id
    AND
    city.id_country = country.id
    AND
    country.name = "France";
```

## Requête 2

But: _Liste des aéroports situés à une certaine distance d'un autre aéroport donné en référence_  

Requête:  
- Version MySQL (avec opérateurs trigonométriques en utilisant le rayon de la Terre)

```sql
SELECT
    b.name
FROM
    airport a,
    airport b
WHERE
    a.name = 'Worms Airport'
    AND (
        ACOS(
            COS(a.latitude * PI() / 180)
            * COS(b.latitude * PI() / 180)
            * COS((b.longitude * PI() / 180)
            - (a.longitude * PI() / 180))
            + SIN(a.latitude * PI() / 180)
            * SIN(b.latitude * PI() / 180)
        ) * 6371
    ) < 100
    AND a.id != b.id;
```

- Version SQL pure (en utilisant la norme du vecteur formé par les deux aéroports)

```sql
SELECT
    b.name
FROM
    airport a,
    airport b
WHERE
    a.name = 'Worms Airport'
    AND (
        ABS(a.latitude - b.latitude)
        - ABS(a.longitude - b.longitude)
    ) * 111.32 <= 100
    AND a.id != b.id;
```

### Requête 3

But: _La durée moyenne des vols à destination de Paris utilisant un A380_  

Requête:  
Ne disposant d'aucune information sur la durée de vol ou la vitesse de chacun des appareils, cette requête n'est pas réalisable par simple requêtage de la base de données.

### Requête 4

But: _Le vol le plus court et le plus long à destination de New York_

Requête:  
N'ayant aucune information sur le distance des vols (comme dit précédement), cette requête n'était pas réalisable. De plus, le rôle d'une base et d'un sgbd n'est pas d'effectuer ce genre de traitements et algorithmes, il en relève du back office.

### Requête 5

But: _Le vol avec le plus d'escales dans un même pays_

Requête:  

```sql
SELECT
   a.id, co.name, COUNT(s.id)
FROM
    airway a,
    step_in s,
    airport ai,
    city ci,
    country co
WHERE
    s.id_airway = a.id
    AND
    s.id_airport = ai.id
    AND
    ai.id_city = ci.id
    AND
    ci.id_country = co.id
GROUP BY a.id, co.id
ORDER BY COUNT(s.id) DESC;
```

### Requête 6

But: _La liste ordonnées des paires de companies qui collaborent le plus sur les trajets avec escale_

Requête:  
Nous n'avons pas de moyens de suivre un vol à travers différentes escales s'il emprunte différentes compagnies. Ainsi, il nous est impossible de réaliser cette requête.

### Requête 7

But: _Par pays, la liste des compagnies qui sont présentes dans tous les aéroports ou à défaut la compagnie la plus présente_

Requête:  

_Non réalisée_

## Partie II: communication C

### Installation

Se rendre dans la partie du projet correspondante, et executer le `Makefile`.


### Organisation du projet

- `main.c` sert de point d'accès à cette partie du projet
- `dal/` regroupe les outils de communication avec la base de données
- `tcp/` regroupe des valeurs remarquables utilisées dans le projet (pour les erreurs par exemple)
- `log/` regroupe les outils permettant de logger des valeurs ou textes dans la console
- `client/` et `server/` regroupent la logique propre à chaque membre destiné à communiquer sur le réseau
- `algorithms/` regroupe la structure de graph utilisée ainsi que les outils qui l'accompagne; mais aussi l'implémentation de _a\*_ et _dijkstra_

## Partie III:

_non communiquée_
