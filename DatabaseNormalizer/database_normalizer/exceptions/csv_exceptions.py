# -*- coding: utf-8 -*-
"""
    database_normalizer.exception.csv_exceptions
    --------------------------------------------

    Custom exceptions for CSV operations.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""

class BadFileFormatException(Exception):
    """Thrown whenever a file with the wrong format is encountered
    """
    pass
