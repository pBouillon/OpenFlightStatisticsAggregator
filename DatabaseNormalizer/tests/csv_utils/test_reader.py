# -*- coding: utf-8 -*-
"""
    tests.csv_utils.reader
    ----------------------

    Test suite for `db_normalizer.csv_utils.reader`.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""

from unittest import TestCase

from pathlib2 import Path

from db_normalizer.csv_utils.reader import Reader
from db_normalizer.csv_utils.utils import Csv
from tests.csv_utils.utils import FileUtils


class TestReader(TestCase):
    """References TestReader

    Test suite for the Reader class.

    `Dat` and `Csv` may be used in unit tests because they does not
    contains any logic.
    """

    def setUp(self) -> None:
        """Initializing the object to test
        """
        # dummy simple csv for tests purpose
        self.dummy_csv = Path(FileUtils.Csv.CSV_NAME)
        self.dummy_csv.touch()
        self.dummy_csv.write_text(FileUtils.Csv.CSV_CONTENT)

        # dummy complex csv for tests purpose
        self.dummy_complex_csv = Path(FileUtils.Csv.ComplexCsv.CSV_NAME)
        self.dummy_complex_csv.touch()
        self.dummy_complex_csv.write_text(
            Csv.separator.join(
                FileUtils.Csv.ComplexCsv.COMPLEX_FIELDS
            )
        )

    def tearDown(self) -> None:
        """Reinitialize state after unit tests execution
        """
        self.dummy_csv.unlink()
        self.dummy_complex_csv.unlink()

    def test_invalid_initialization_unknown_file(self):
        """A non-existing file should throw an exception
        """
        with self.assertRaises(FileNotFoundError):
            Reader(FileUtils.Csv.NON_EXISTING_NAME)

    def test_valid_properties_columns(self):
        """The reader should correctly get the columns number
        """
        # arrange
        expected = len(
            FileUtils.Csv.CSV_CONTENT
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
            FileUtils.Csv.CSV_CONTENT
            .split(Csv.line_end)
        )

        # act
        reader = Reader(str(self.dummy_csv))

        # assert
        self.assertEqual(
            expected,
            reader.rows
        )

    def test_valid_read_content(self):
        """The reader should correctly gather the fields
        """
        # arrange
        expected_len = len(FileUtils.Csv.ComplexCsv.COMPLEX_FIELDS)
        reader = Reader(str(self.dummy_complex_csv))

        # act
        # read the content of the file
        content = list(reader.read_content())
        # only stores the first line
        content = content[0]

        # assert
        # the length of the content read should be the same as specified
        self.assertEqual(
            expected_len,
            len(content)
        )
        # the files writen and loaded should be the same
        self.assertListEqual(
            FileUtils.Csv.ComplexCsv.COMPLEX_FIELDS,
            content
        )
