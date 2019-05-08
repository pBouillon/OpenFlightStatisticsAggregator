# -*- coding: utf-8 -*-
"""
    db_normalizer.db_normalizer
    ---------------------------------------

    Launch point for the db_normalizer project.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
import time
from typing import List

from db_normalizer.csv_handler.normalizer import Normalizer
from db_normalizer.csv_handler.utils import Dat
from db_normalizer.dal.dal import Dal
from db_normalizer.data_loader.loader import Loader
from db_normalizer.dal.utils import DatabaseUtils


"""program's current version"""
__version__ = '1.9.2'


def pretty_print_collection(name: str, collection: List) -> None:
    """

    :param name:
    :param collection:
    :return:
    """
    print(f'\t- {name: >12}: {len(collection): >8}')


def show_header() -> None:
    """program's startup header
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


def main():
    """program's logic execution
    """
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
    print(f'[INFO] done in {(time.time() - begin):1.3f} second.s\n')

    #
    # Load data in the loader
    print('[INFO] initializing loader ...')
    begin = time.time()
    loader = Loader()
    print(f'[INFO] done in {(time.time() - begin):1.3f} second.s\n')

    # Extracting data
    print('[INFO] extracting data ...')
    begin = time.time()
    loader.load_all_raw()
    print(
        f'[INFO] {loader.records} records loaded in '
        f'{(time.time() - begin):1.3f} second.s\n'
    )

    # Fetching additional data
    if input(
        '[WARN] Do you want to load external data ?\n'
        '[WARN] (fetching external resources take a huge amount of time)\n'
        '[WARN] (y/N) -> '
    ) == 'y':
        print('[INFO] fetching external data...')
        begin = time.time()
        loader.load_external(smooth=True)
        print(
            f'[INFO] external data loaded in '
            f'{(time.time() - begin):1.3f} second.s'
        )
    print()

    #
    # Show loaded data info
    print('Recorded:')
    [
        pretty_print_collection(name, collection)
        for name, collection
        in loader.records_lists.items()
    ]
    print()

    #
    # Initiate a database connection
    dal = Dal()

    # Create tables
    begin = time.time()
    dal.create_tables()
    print(
        f'[INFO] tables created in '
        f'{(time.time() - begin):1.3f} second.s'
    )

    # Load tracked records in the database
    begin = time.time()
    dal.write_from_loader(loader)
    print(
        f'[INFO] records stored in database in '
        f'{(time.time() - begin):1.3f} second.s'
    )

    # Dumps the sql
    begin = time.time()
    dal.dump_content()
    print(
        f'[INFO] SQL dump created in \'{DatabaseUtils.sqlitedb_dump}\' in '
        f'{(time.time() - begin):1.3f} second.s\n'
    )


if __name__ == '__main__':
    # Displays program's startup
    show_header()

    # execute logic
    main()
