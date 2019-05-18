# -*- coding: utf-8 -*-
"""
    db_normalizer.dal.sql_bridge
    ----------------------------

    Store connection data to establish a connection with the Oracle database.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""


class DatabaseUtils:
    """References ConnectionData
    """

    """username for the database connection"""
    username = 'grpA2'

    """hostname for the database connection"""
    hostname = 'oracle.telecomnancy.univ-lorraine.fr'

    """password for the database connection"""
    password = 'TPOracle'

    """port for the database connection"""
    port = 1521

    """service name for the database connection"""
    service_name = 'TNCY'

    """destination for the sqlite3 temp database"""
    sqlite_db = ':memory:'

    """default path to dumb the sql"""
    sqlitedb_dump = '../static/sql/sql_dump/generated_sql.sql'

    """table schemas"""
    sql_tables_path = '../static/sql/sqlite_sources'

    """sql default file extension"""
    sql_extension = '.sql'
