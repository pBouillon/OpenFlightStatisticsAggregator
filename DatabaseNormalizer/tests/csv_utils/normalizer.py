# -*- coding: utf-8 -*-
"""
    tests.csv_utils.normalizer
    --------------------------

    Test suite for `database_normalizer.csv_utils.normalizer`.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
from unittest import TestCase

from pathlib2 import Path

from csv_utils.normalizer import Normalizer
from csv_utils.utils import Dat
from exceptions.csv_exceptions import BadFileFormatException


class TestNormalizer(TestCase):
    """References TestNormalizer

    Test suite for the Normalizer class

    `Dat` and `Csv` may be used in unit tests because they does not
    contains any logic
    """

    """Dummy dat name for tests purpose"""
    DUMMY_CSV = 'dummy_csv.csv'

    """Dummy csv name for tests purpose"""
    DUMMY_DAT = 'dummy_dat.dat'

    """Dummy placeholder for a non-existing resource"""
    NON_EXISTING_NAME = 'this_does_not_exists/'

    def setUp(self) -> None:
        """Initializing the object to test
        """
        self.normalizer = Normalizer(
            to_normalize_ext=Dat.ext,
            separator=Dat.separator
        )
        self.dummy_csv = Path(self.DUMMY_CSV)
        self.dummy_csv.touch()

        self.dummy_dat = Path(self.DUMMY_DAT)
        self.dummy_dat.touch()

    def tearDown(self) -> None:
        """Reinitialize state after unit tests execution
        """
        self.dummy_csv.unlink()
        self.dummy_dat.unlink()

    def test_invalid_is_valid_csv_field_number(self):
        """A bad formatted number should be invalid
        """
        # trailing quotes
        self.assertFalse(Normalizer.is_valid_csv_field('1337"'))
        # beginning quotes
        self.assertFalse(Normalizer.is_valid_csv_field('"1337'))
        # no quotes
        self.assertFalse(Normalizer.is_valid_csv_field('1337'))

    def test_valid_is_valid_csv_field_number(self):
        """A well formatted number should be valid
        """
        # int
        self.assertTrue(Normalizer.is_valid_csv_field('"42"'))
        # float
        self.assertTrue(Normalizer.is_valid_csv_field('"13.37"'))
        # negative
        self.assertTrue(Normalizer.is_valid_csv_field('"-3.14"'))

    def test_valid_is_valid_csv_field_string(self):
        """A well formatted string should be valid
        """
        # single string
        self.assertTrue(Normalizer.is_valid_csv_field('"field"'))
        # with spaces
        self.assertTrue(Normalizer.is_valid_csv_field('"some field"'))

    def test_invalid_convert_to_csv_no_file(self):
        """A non-existing file should throw an exception
        """
        # with an incorrect extension too
        with self.assertRaises(FileNotFoundError):
            self.normalizer.convert_to_csv(dat_path=self.NON_EXISTING_NAME)

        # with the appropriate extension
        with self.assertRaises(FileNotFoundError):
            self.normalizer.convert_to_csv(
                dat_path=self.NON_EXISTING_NAME + Dat.ext
            )

    def test_invalid_convert_to_csv_bad_file_dat_ext(self):
        """A bad DAT file extension should throw an exception
        """
        with self.assertRaises(BadFileFormatException):
            self.normalizer.convert_to_csv(dat_path=str(self.dummy_csv))

    def test_invalid_convert_to_csv_bad_file_dat_csv(self):
        """A bad CSV file extension should throw an exception
        """
        with self.assertRaises(BadFileFormatException):
            self.normalizer.convert_to_csv(
                dat_path=str(self.dummy_dat),
                csv_path=str(self.dummy_dat)
            )

    def test_invalid_convert_to_csv_from_folder_non_existing_folder(self):
        """A non-existing folder should throw an exception
        """
        with self.assertRaises(BadFileFormatException):
            self.normalizer.convert_to_csv_from_folder(
                dat_folder=self.NON_EXISTING_NAME
            )

    def test_invalid_convert_to_csv_from_folder_not_folder(self):
        """A non-existing folder should throw an exception
        """
        with self.assertRaises(BadFileFormatException):
            self.normalizer.convert_to_csv_from_folder(
                dat_folder=self.dummy_dat
            )