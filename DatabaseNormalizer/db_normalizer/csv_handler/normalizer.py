# -*- coding: utf-8 -*-
"""
    db_normalizer.csv_handler.normalizer
    ----------------------------------------

    Allow the user to convert .dat files to .csv.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
import re
from typing import List, Iterator, Optional

from pathlib2 import Path

from db_normalizer.csv_handler.utils import Dat, Csv, Parsing
from db_normalizer.exceptions.csv_exceptions import BadFileFormatException


class Normalizer:
    """References Normalizer

    Normalize a file with a file to .csv.
    """

    """Default folder for csv files"""
    DEFAULT_OUTPUT_FOLDER = '../static/data/csv_files/'

    def __init__(
            self,
            to_normalize_ext: Optional[str] = Dat.ext,
            separator: Optional[str] = Dat.separator,
    ):
        """Constructor

        :param to_normalize_ext: extension of the files to normalize
        :param separator: separator of the parsed files
        """
        self._to_normalize_ext = to_normalize_ext
        self._separator = separator

    @staticmethod
    def is_valid_csv_field(field: str) -> bool:
        """Check whether a field is a valid csv field or not

        :param field: field to check
        :return: True if valid; False otherwise
        """
        return field.startswith(Csv.delimiter) \
            and field.endswith(Csv.delimiter)

    def _format_dirty_content(self, content: List[str]) -> Iterator[str]:
        """Format non-csv content

        Read the `content` line per line
        Then break it down in several fields
        Finally return a generator with formatted csv rows

        :param content: the non-csv content
        :return: a generator with lines formatted
        """
        for line in content:
            formatted_line: List[str] = []

            # for each field in the row
            for field, _ in re.findall(
                Parsing.parse_regex,
                line
            )[:-1]:
                # removing trailing '\n'
                field = field.rstrip()

                # formatting the field if needed
                if not self.is_valid_csv_field(field):
                    field = Csv.delimiter \
                            + field.replace('"', '""') \
                            + Csv.delimiter

                # adding the field to the current row
                formatted_line.append(field)

            # add the line to the generator
            yield Csv.separator.join(formatted_line) + Csv.line_end

    def convert_to_csv(
            self,
            dat_path: str,
            csv_path: Optional[str] = ''
    ) -> None:
        """Convert a .dat file to csv

        Check whether the .dat file exists
        Then read it
        Finally store its .csv equivalent

        :see: https://tools.ietf.org/html/rfc4180

        :param dat_path: path to the .dat file
        :param csv_path: name and location of the generated .csv file
        :return: None
        """
        # checking source file integrity
        source = Path(dat_path)
        if not source.exists():
            raise FileNotFoundError

        if source.suffix != Dat.ext:
            raise BadFileFormatException(
                f'source file should contains the extension: '
                f'{Dat.ext}'
            )

        # checking output file integrity
        if not csv_path:
            csv_path = f'{self.DEFAULT_OUTPUT_FOLDER}' \
                f'{source.name.replace(Dat.ext, Csv.ext)}'
        else:
            if not csv_path.endswith(Csv.ext):
                raise BadFileFormatException(
                    f'output should contains the extension: '
                    f'{Csv.ext}'
                )
        output = Path(csv_path)

        if not output.exists():
            output.touch()

        # formatting content
        with source.open(mode='r', encoding=Dat.encoding) as src:
            content = src.readlines()

        # writing the formatted content
        with output.open(mode='w', encoding=Csv.encoding) as dest:
            for row in self._format_dirty_content(content):
                dest.write(row)

    def convert_to_csv_from_folder(
            self,
            dat_folder: str,
            csv_folder: Optional[str] = None
    ) -> None:
        """Convert all dat in a folder to csv

        Iterate over the given folder
        Then normalize each .dat file found to .csv

        :param dat_folder: folder containing .dat files
        :param csv_folder: folder in which store CSV
        :return: None
        """
        folder = Path(dat_folder)

        if not folder.exists() \
                or not folder.is_dir():
            raise BadFileFormatException

        if not csv_folder:
            csv_folder = self.DEFAULT_OUTPUT_FOLDER

        for file in folder.iterdir():
            if file.suffix != Dat.ext:
                continue

            self.convert_to_csv(
                dat_path=str(file),
                csv_path=f'{csv_folder}{file.name.replace(Dat.ext, Csv.ext)}'
            )
