# -*- coding: utf-8 -*-
"""
    database_normalizer.database_normalizer
    ---------------------------------------

    Launch point for the database_normalizer project.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""

from csv_utils.normalizer import Normalizer
from csv_utils.utils import Dat

__version__ = '0.2.0'


if __name__ == '__main__':
    print(f'Current version: {__version__}')

    # Creating the normalizer object for .dat files
    normalizer = Normalizer(
        to_normalize_ext=Dat.ext,
        separator=Dat.separator
    )

    # Normalizing each .dat files in the data folder
    normalizer.convert_to_csv_from_folder(
        dat_folder='../static/data/dat_files'
    )
