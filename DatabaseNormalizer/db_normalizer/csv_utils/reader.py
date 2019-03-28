# -*- coding: utf-8 -*-
"""
    db_normalizer.csv_utils.reader
    ----------------------------------------

    Reading toolbox for .csv files.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
import re
from typing import List, Iterator, Optional

from pathlib2 import Path

from db_normalizer.csv_utils.utils import Csv, Parsing


class Reader:
    """References Reader

    Pleasant interface for .csv reading.
    """

    def __init__(self, file_path: str):
        """Constructor

        :param file_path: path to the csv file
        """
        self._file_path = file_path
        self._file = Path(file_path)

        if not self._file.exists():
            raise FileNotFoundError

        self._columns = self._rows = -1
        self._load_stats()

    def _load_stats(self) -> None:
        """Load stats of the .csv file for future usage
        """
        self._rows = 0
        for line in self._file.read_text(Csv.encoding).split('\n'):
            if self._columns == -1:
                self._columns = len(line.split(Csv.separator))
            self._rows += 1

    def read_content(
            self,
            skip_header: Optional[bool] = False,
            encoding: Optional[str] = Csv.encoding
    ) -> Iterator[List[str]]:
        """Read .csv content

        :param skip_header:
        :param encoding:
        :return: an iterator with each line as a list of its columns
        """
        is_header_skipped = False

        for line in self._file.read_text(encoding).split('\n'):
            # skipping header if needed
            if skip_header and not is_header_skipped:
                is_header_skipped = True
                continue

            # removing empty lines
            if not line:
                continue

            # from a row, removing trailing \n in all fields
            values = [field for field, _ in re.findall(
                Parsing.parse_regex,
                line
            )][:-1]

            yield list(map(
                    lambda field: field.rstrip(),
                    values
                ))

    @property
    def columns(self) -> int:
        """Getter for `_columns`
        :return: the number of columns in the file
        """
        return self._columns

    @property
    def rows(self) -> int:
        """Getter for `_rows`
        :return: the number of rows in the file
        """
        return self._rows
