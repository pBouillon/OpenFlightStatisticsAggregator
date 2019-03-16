# -*- coding: utf-8 -*-
"""
    database_normalizer.csv_utils.normalizer
    ----------------------------------------

    Allow the user to convert .dat files to .csv.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""

from pathlib2 import Path

from Exceptions.csv_exceptions import BadFileFormatException
from csv_utils.utils import Csv, Dat


"""Default folder for csv files"""
DEFAULT_OUTPUT_FOLDER = '../static/data/csv_files/'

def convert_to_csv_from_folder(
        dat_folder: str,
        separator: str,
        csv_folder: str = None
) -> None:
    """Convert all dat in a folder to csv

    :param dat_folder: folder containing .dat files
    :param separator:  .dat file delimiter
    :param csv_folder: folder in which store CSV
    :return: None
    """
    folder = Path(dat_folder)

    if not folder.exists() \
            or not folder.is_dir():
        raise BadFileFormatException

    if not csv_folder:
        csv_folder = DEFAULT_OUTPUT_FOLDER

    for file in folder.iterdir():
        if file.suffix != Dat.ext:
            continue

        convert_to_csv(
            dat_path=str(file),
            separator=separator,
            csv_path=f'{csv_folder}{file.name[:-len(Dat.ext)]}{Csv.ext}'
        )


def convert_to_csv(
        dat_path: str,
        separator: str,
        csv_path: str = ''
) -> None:
    """Convert a .dat file to csv

    Check whether the .dat file exists
    Then read it
    Finally store its .csv equivalent

    :see: https://tools.ietf.org/html/rfc4180

    :param dat_path: path to the .dat file
    :param separator: .dat file delimiter
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
        csv_path = f'{DEFAULT_OUTPUT_FOLDER}' \
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

    with output.open(mode='w', encoding=Csv.encoding) as dest:
        for line in content:
            formatted_line:list = []

            # for each field in the row
            for field in line.split(separator):
                field = field.rstrip()

                # if the field is surrounded by the
                # appropriate delimiter add it
                if field.startswith(Csv.delimiter) \
                        and field.endswith(Csv.delimiter):
                    formatted_line.append(field)

                # else manually add the delimiters
                else:
                    formatted_line.append(
                        Csv.delimiter
                        + field.replace('"', '""')
                        + Csv.delimiter
                    )

            # add the line
            dest.write(Csv.separator.join(formatted_line) + Csv.line_end)
