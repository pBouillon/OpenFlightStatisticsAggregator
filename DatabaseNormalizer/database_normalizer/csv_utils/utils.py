# -*- coding: utf-8 -*-
"""
    database_normalizer.csv_utils.utils
    ----------------------------------------

    Store useful data to operate on CSV files.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""


class Csv:
    """References CSV data
    """

    """CSV field delimiter"""
    delimiter = '"'

    """CSV file default encoding"""
    encoding = 'utf-8'

    """CSV file extension"""
    ext = '.csv'

    """Csv line ending"""
    line_end = '\n'

    """CSV separator"""
    separator = ','


class Dat:
    """References DAT data
    """

    """DAT file default encoding"""
    encoding = 'utf-8'

    """DAT file extension"""
    ext = '.dat'

    """DAT separator"""
    separator = ','
