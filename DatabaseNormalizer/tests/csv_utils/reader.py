# -*- coding: utf-8 -*-
"""
    tests.csv_utils.reader
    ----------------------

    Test suite for `database_normalizer.csv_utils.reader`.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""

from unittest import TestCase

from pathlib2 import Path

from DatabaseNormalizer.tests.csv_utils.utils import FileUtils
from csv_utils.reader import Reader
from csv_utils.utils import Csv


class TestReader(TestCase):
    """References TestReader

    Test suite for the Reader class.

    `Dat` and `Csv` may be used in unit tests because they does not
    contains any logic.
    """

    def setUp(self) -> None:
        """Initializing the object to test
        """
        self.dummy_csv = Path(FileUtils.DUMMY_CSV)
        self.dummy_csv.touch()
        self.dummy_csv.write_text(FileUtils.DUMMY_CSV_CONTENT)

    def tearDown(self) -> None:
        """Reinitialize state after unit tests execution
        """
        self.dummy_csv.unlink()

    def test_invalid_initialization_unknown_file(self):
        """A non-existing file should throw an exception
        """
        with self.assertRaises(FileNotFoundError):
            Reader(FileUtils.NON_EXISTING_NAME)

    def test_valid_properties_columns(self):
        """The reader should correctly get the columns number
        """
        # arrange
        expected = len(
            FileUtils.DUMMY_CSV_CONTENT
            .split(Csv.line_end)[0]
            .split(Csv.separator)
        )

        # act
        reader = Reader(str(self.dummy_csv))

        # assert
        self.assertEqual(
            expected,
            reader.columns
        )

    def test_valid_properties_rows(self):
        """The reader should correctly get the columns number
        """
        # arrange
        expected = len(
            FileUtils.DUMMY_CSV_CONTENT
            .split(Csv.line_end)
        )

        # act
        reader = Reader(str(self.dummy_csv))

        # assert
        self.assertEqual(
            expected,
            reader.rows
        )
