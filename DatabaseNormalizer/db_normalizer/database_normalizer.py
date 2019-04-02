# -*- coding: utf-8 -*-
"""
    db_normalizer.db_normalizer
    ---------------------------------------

    Launch point for the db_normalizer project.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
import time

from db_normalizer.csv_handler.normalizer import Normalizer
from db_normalizer.csv_handler.utils import Dat
from db_normalizer.data_loader.loader import Loader

__version__ = '1.4.0'


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
        '**',
        '**  Url: ',
        '**     https://gitlab.telecomnancy.univ-lorraine.fr/ppii-2k19/project-grpa2',
        '*****\n',
    ]))


if __name__ == '__main__':
    # Displays program's startup
    show_header()

    #
    # Creating the normalizer object for .dat files
    print('[INFO] normalizing .dat files ...')
    begin = time.time()
    normalizer = Normalizer(
        to_normalize_ext=Dat.ext,
        separator=Dat.separator
    )

    # Normalizing each .dat files in the data folder
    normalizer.convert_to_csv_from_folder(
        dat_folder='../static/data/dat_files'
    )
    print(f'[INFO] done in {(time.time() - begin):1.5f} second.s\n')

    #
    # Load data in the loader
    print('[INFO] initializing loader ...')
    begin = time.time()
    loader = Loader()
    print(f'[INFO] done in {(time.time() - begin):1.5f} second.s\n')

    # Extracting data
    print('[INFO] extracting data ...')
    begin = time.time()
    loader.load_all()
    print(f'[INFO] done in {(time.time() - begin):1.5f} second.s\n')

    #
    # Show loaded data info
    print(f'{len(loader.dst_records)} DSTs recorded')
    print(f'{len(loader.airway_records)} airways recorded')
