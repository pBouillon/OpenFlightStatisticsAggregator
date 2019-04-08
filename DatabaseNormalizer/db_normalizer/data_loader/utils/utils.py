# -*- coding: utf-8 -*-
"""
    db_normalizer.data_loader.utils
    -------------------------------

    Store useful data to extract data from the CSV files.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
from db_normalizer.csv_handler.utils import Csv


class Sources:
    """References sources data
    """

    """base folder in which the data files are stored"""
    _base_folder = '../static/data/csv_files/'

    """path to the airports csv file"""
    airports = _base_folder + 'airports' + Csv.ext

    """path to the airlines csv file"""
    airlines = _base_folder + 'airlines' + Csv.ext

    """path to the flight_numbers csv file"""
    flight_numbers = _base_folder + 'flightnumbers' + Csv.ext

    """path to the planes csv file"""
    planes = _base_folder + 'planes' + Csv.ext

    """path to the route csv file"""
    routes = _base_folder + 'routes' + Csv.ext
