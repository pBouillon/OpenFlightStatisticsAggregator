# -*- coding: utf-8 -*-
"""
    database_normalizer.data_injector.injector
    ------------------------------------------

    From the relevant .csv, generate scripts to fill the tables.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from typing import List, Dict

from pathlib2 import Path

from DatabaseNormalizer.database_normalizer\
    .exceptions.csv_exceptions import BadFileFormatException


class Injector:
    """References Injector

    """

    """"""
    DEFAULT_OUTPUT_FOLDER = '../static/scripts/sql_inserts/'
    """"""
    DEFAULT_SOURCE_FOLDER = '../static/data/csv_files/'

    def __init__(
            self,
            csv_folder: str = DEFAULT_SOURCE_FOLDER,
            dest_folder: str = DEFAULT_OUTPUT_FOLDER
    ):
        """Initialize the generator for the sql rows injection

        :raise BadFileFormatException:
        :param csv_folder: should contains the csv sources with files:
                           `airlines`, `airports`, `planes`, `routes`
        :param dest_folder: existing folder in which place the generated sql
                            insertion scripts
        """
        self._dest_dir = Path(dest_folder)
        self._src_dir = Path(csv_folder)

        if not all(
            f.exists() or f.is_dir()
            for f in [self._dest_dir, self._src_dir]
        ):
            raise BadFileFormatException(
                'Parameters should be existing folders.'
            )

        self._records: Dict[str, List[dataclass]] = {
            'airlines': [],
            'airports': [],
            'airways': [],
            'cities': [],
            'countries': [],
            'dst': [],
            'fly_on': [],
            'iata': [],
            'icao': [],
            'planes': [],
            'plane_types': [],
            'timezones': [],
        }

    @staticmethod
    def _get_dataclass_sql_values(to_parse: dataclass) -> str:
        """Read the dataclass attributes and return them

        Return the dataclass attributes as:
            number,"str",number, etc .
        Strings are wrapped in double quotes

        Example:
            "Chicago",26,0.3,"GMT"

        :param to_parse:
        :return: the attributes, separated with commas
        """
        sql = ''

        for _, value in to_parse.__dict__.items():
            if type(value) is str:
                sql += f'"{value}"'
            else:
                sql += f"{value}"
            sql += ','

        return sql[:-1]

    def gen_sql_inserts(self) -> None:
        """

        :return:
        """
        pass
