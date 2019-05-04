# -*- coding: utf-8 -*-
"""
    db_normalizer.dal.sql_bridge
    ----------------------------

    Bridge between the application and the Oracle database.

    /!\\ WiP /!\\

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
import atexit
import sqlite3

from db_normalizer.dal.utils import DatabaseUtils
from db_normalizer.data_loader.loader import Loader


class Dal:
    """Reference the data access layer
    """

    def __init__(self):
        self._connection = None
        self._cursor = None

        self._initiate_connection()
        atexit.register(self._close_connection)

    def _close_connection(self) -> None:
        """Close the connection

        Note: the cursor is garbage collected
        """
        self._connection.close()

    def _initiate_connection(self) -> None:
        """Initiate the connection

        Create the connection and the cursor bind to it
        """
        self._connection = sqlite3.connect(DatabaseUtils.sqlite_db)
        self._cursor = self._connection.cursor()

    @staticmethod
    def dataclass_to_list(dataclass) -> list:
        """Convert a dataclass to a list

        :param dataclass: the dataclass from which extract the data
        :return: a list of all its attributes values
        """
        return list(dataclass.__dict__.values())

    def create_tables(self) -> None:
        """Create all tables from their schemas

        :see DatabaseUtils.sql_tables:
        """
        for table_schema in DatabaseUtils.sql_tables:
            self._cursor.execute(table_schema)
        self._connection.commit()

    def dump_content(self, dest: str = DatabaseUtils.sqlitedb_dump) -> None:
        """Dump the database content to a file

        :param dest: destination for the dumped sql
        """
        with open(dest, 'w') as f:
            for line in self._connection.iterdump():
                f.write(f'{line}\n')

    def write_from_loader(self, loader: Loader) -> None:
        """Write in database all loaded data

        :param loader: loader object containing all the data
        """
        # transition functions to write all records of a single dataclass type
        def write_dst() -> None:
            self._cursor.executemany(
                'INSERT INTO DST VALUES (?, ?)',
                [
                    Dal.dataclass_to_list(record)
                    for record in loader.dst_records
                ]
            )
            self._connection.commit()

        def write_timezone() -> None:
            self._cursor.executemany(
                'INSERT INTO TIMEZONE VALUES (?, ?, ?)',
                [
                    Dal.dataclass_to_list(record)
                    for record in loader.timezone_records
                ]
            )
            self._connection.commit()

        def write_plane_type() -> None:
            self._cursor.executemany(
                'INSERT INTO PLANE_TYPE VALUES (?, ?, ?)',
                [
                    Dal.dataclass_to_list(record)
                    for record in loader.plane_type_records
                ]
            )
            self._connection.commit()

        def write_plane() -> None:
            self._cursor.executemany(
                'INSERT INTO PLANE VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                [
                    Dal.dataclass_to_list(record)
                    for record in loader.plane_records
                ]
            )
            self._connection.commit()

        def write_country() -> None:
            self._cursor.executemany(
                'INSERT INTO COUNTRY VALUES (?, ?, ?, ?)',
                [
                    Dal.dataclass_to_list(record)
                    for record in loader.country_records
                ]
            )
            self._connection.commit()

        def write_city() -> None:
            self._cursor.executemany(
                'INSERT INTO CITY VALUES (?, ?, ?, ?)',
                [
                    Dal.dataclass_to_list(record)
                    for record in loader.city_records
                ]
            )
            self._connection.commit()

        def write_airline() -> None:
            self._cursor.executemany(
                'INSERT INTO AIRLINE VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                [
                    Dal.dataclass_to_list(record)
                    for record in loader.airline_records
                ]
            )
            self._connection.commit()

        def write_airport() -> None:
            self._cursor.executemany(
                'INSERT INTO AIRPORT VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                [
                    Dal.dataclass_to_list(record)
                    for record in loader.airport_records
                ]
            )
            self._connection.commit()

        def write_use() -> None:
            self._cursor.executemany(
                'INSERT INTO USE VALUES (?, ?)',
                [
                    Dal.dataclass_to_list(record)
                    for record in loader.use_records
                ]
            )
            self._connection.commit()

        def write_step_in() -> None:
            self._cursor.executemany(
                'INSERT INTO STEP_IN VALUES (?, ?)',
                [
                    Dal.dataclass_to_list(record)
                    for record in loader.step_in_records
                ]
            )
            self._connection.commit()

        # load the database by order of dependencies
        write_dst()
        write_timezone()
        write_plane_type()
        write_plane()
        write_country()
        write_city()
        write_airline()
        write_airport()
        write_use()
        write_step_in()

