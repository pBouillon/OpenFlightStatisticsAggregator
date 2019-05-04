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


class Dal:
    """Reference the data access layer
    """

    def __init__(self):
        self._connection = None
        self._cursor = None

        self._initiate_connection()
        atexit.register(self._close_connection)

    def _initiate_connection(self):
        """Initiate the connection

        Create the connection and the cursor bind to it
        """
        self._connection = sqlite3.connect(DatabaseUtils.sqlite_db)
        self._cursor = self._connection.cursor()

    def _close_connection(self):
        """Close the connection

        Note: the cursor is garbage collected
        """
        self._connection.close()

    def create_tables(self):
        """Create all tables from their schemas

        :see DatabaseUtils.sql_tables:
        """
        for table_schema in DatabaseUtils.sql_tables:
            self._cursor.execute(table_schema)
        self._connection.commit()
    
    def dump_content(self, dest: str = DatabaseUtils.sqlitedb_dump):
        """Dump the database content to a file

        :param dest: destination for the dumped sql
        """
        with open(dest, 'w') as f:
            for line in self._connection.iterdump():
                f.write(f'{line}\n')


if __name__ == '__main__':
    dal = Dal()
    dal.create_tables()
