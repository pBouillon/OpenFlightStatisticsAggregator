# -*- coding: utf-8 -*-
"""
    database_normalizer.database_normalizer
    ---------------------------------------

    Launch point for the database_normalizer project.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""

from csv_utils.normalizer import Normalizer
from csv_utils.reader import Reader
from csv_utils.utils import Dat

__version__ = '0.3.0'


def show_header() -> None:
    """Program's startup header
    """
    print('\n'.join([
        '*****',
        '**  - Projet PPII - ',
        f'**  Version:  {__version__}',
        '**',
        '**  Auteurs: ',
        '**     BOUILLON Pierre, CESARI Alexandre',
        '**  Url: ',
        '**     https://gitlab.telecomnancy.univ-lorraine.fr/ppii-2k19/project-grpa2',
        '**',
        '*****\n',
    ]))


if __name__ == '__main__':
    # Displays program's startup
    show_header()

    # Creating the normalizer object for .dat files
    normalizer = Normalizer(
        to_normalize_ext=Dat.ext,
        separator=Dat.separator
    )

    # Normalizing each .dat files in the data folder
    normalizer.convert_to_csv_from_folder(
        dat_folder='../static/data/dat_files'
    )

    # Read one of them
    reader = Reader('../static/data/csv_files/airlines.csv')
    print(f'The file contains {reader.rows} rows and {reader.columns} columns')
