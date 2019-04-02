# -*- coding: utf-8 -*-
"""
    tests.csv_handler.utils
    ---------------------

    Dummy data for unit tests.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""


class FileUtils:
    """References files data toolbox
    """

    class Csv:
        """References Csv
        """

        """Dummy csv name for tests purpose"""
        CSV_NAME = 'dummy_csv.csv'

        """Dummy csv content for tests purpose"""
        CSV_CONTENT = \
            '"Some","Body","I"\n' \
            '"Used","To","Know"'

        """Dummy dat name for tests purpose"""
        DAT_NAME = 'dummy_dat.dat'

        """Dummy placeholder for a non-existing resource"""
        NON_EXISTING_NAME = 'this_does_not_exists/'

        class ComplexCsv:
            """References ComplexCsv
            """

            """Dummy csv name for tests purpose"""
            CSV_NAME = 'dummy_complex_csv.csv'

            """Tricky csv fields to parse"""
            COMPLEX_FIELDS = [
                'some body',
                '"I, used"',
                '"to" know"'
            ]
