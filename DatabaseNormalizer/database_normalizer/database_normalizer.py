# -*- coding: utf-8 -*-
"""
    database_normalizer.database_normalizer
    ---------------------------------------

    Launch point for the database_normalizer project.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""

from csv_utils import normalizer
from csv_utils.utils import Dat

__version__ = '0.1.0'


if __name__ == '__main__':
    print(f'Current version: {__version__}')

    normalizer.convert_to_csv_from_folder(
        dat_folder='../static/data/dat_files',
        separator=Dat.separator
    )
