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

__version__ = '1.8.4'


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
    loader.load_all_raw()
    print(
        f'[INFO] {loader.records} records loaded in '
        f'{(time.time() - begin):1.5f} second.s\n'
    )

    # Fetching additional data
    if input(
        '[WARN] Do you want to load external data ?\n'
        '[WARN] (fetching external resources take a huge amount of time)\n'
        '[WARN] (y/N) -> \n'
    ) == 'y':
        print('[INFO] fetching external data...')
        begin = time.time()
        loader.load_external(smooth=True)
        print(
            f'[INFO] external data loaded in '
            f'{(time.time() - begin):1.5f} second.s\n'
        )

    #
    # Show loaded data info
    print('Recorded:')
    print(f'\t{len(loader.airline_records):6}{"":4}Airlines')
    print(f'\t{len(loader.airport_records):6}{"":4}Airports')
    print(f'\t{len(loader.airway_records):6}{"":4}Airways')
    print(f'\t{len(loader.city_records):6}{"":4}Cities')
    print(f'\t{len(loader.country_records):6}{"":4}Countries')
    print(f'\t{len(loader.dst_records):6}{"":4}DSTs')
    print(f'\t{len(loader.plane_records):6}{"":4}Planes')
    print(f'\t{len(loader.plane_type_records):6}{"":4}Plane types')
    print(f'\t{len(loader.timezone_records):6}{"":4}Timezones')
