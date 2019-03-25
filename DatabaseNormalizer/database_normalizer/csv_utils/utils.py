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


class Parsing:
    """Regex to parse the dat file

        (?:^||,)        starting at the beginning of the file or with a comma
        \s*             followed by no or many spaces
        (
            ("[^"]*")   capturing fields surrounded by double quotes
            |           or
            [^,]*       capturing fields with no quotes containing no commas
        )
        \s*             followed by no or many spaces
        (?:,\s*|$)      ending with a comma and spaces or the end of the line
        """
    parse_regex = r'(?:^||,)\s*(("[^"]*")|[^,]*)\s*(?:,\s*|$)'
