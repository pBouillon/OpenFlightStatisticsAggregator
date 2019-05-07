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
    sqlitedb_dump = '../static/sql/dump.sql'

    """table schemas"""
    sql_tables = [
        # airway
        """ CREATE TABLE IF NOT EXISTS AIRWAY (
            id          INTEGER PRIMARY KEY,
            codeshare   TEXT
        ); """,
        # dst
        """CREATE TABLE IF NOT EXISTS DST (
            id          INTEGER PRIMARY KEY,
            name        TEXT
        ); """,
        # timezone
        """CREATE TABLE IF NOT EXISTS TIMEZONE (
            id          INTEGER PRIMARY KEY,
            name        TEXT,
            padding     INTEGER
        ); """,
        # plane type
        """CREATE TABLE IF NOT EXISTS PLANE_TYPE (
            id          INTEGER PRIMARY KEY,
            iata_code   TEXT,
            type        TEXT   
        ); """,
        # plane
        """ CREATE TABLE IF NOT EXISTS PLANE (
            id          INTEGER PRIMARY KEY,
            id_plane_type INTEGER,
            iata_code   TEXT,
            icao_code   TEXT,
            model       TEXT,
            passengers  INTEGER,
            consumption INTEGER,
            freight     INTEGER,
            speed       INTEGER,

            FOREIGN KEY (id_plane_type) REFERENCES PLANE_TYPE(id)
        ); """,
        # country
        """CREATE TABLE IF NOT EXISTS COUNTRY (
            id          INTEGER PRIMARY KEY,
            id_dst      INTEGER,
            name        TEXT,
            area        REAL,
            population  INTEGER,

            FOREIGN KEY (id_dst) REFERENCES DST (id)
        ); """,
        # city
        """CREATE TABLE IF NOT EXISTS CITY (
            id          INTEGER PRIMARY KEY, 
            id_country  INTEGER, 
            id_timezone INTEGER, 
            name        TEXT,
            population  INTEGER, 

            FOREIGN KEY (id_country) REFERENCES COUNTRY (id),
            FOREIGN KEY (id_timezone) REFERENCES TIMEZONE (id)
        ); """,
        # airline
        """CREATE TABLE IF NOT EXISTS AIRLINE (
            id          INTEGER PRIMARY KEY,
            id_country  INTEGER,
            active      BOOLEAN,
            alias       TEXT,
            callsing    TEXT,
            name        TEXT,
            iata_code   TEXT,
            icao_code   TEXT,

            FOREIGN KEY (id_country) REFERENCES COUNTRY (id)
        ); """,
        # airport
        """CREATE TABLE IF NOT EXISTS AIRPORT (
            id          INTEGER PRIMARY KEY,
            id_city     INTEGER,
            altitude    REAL,
            iata_code   TEXT,
            icao_code   TEXT,
            latitude    REAL,
            longitude   REAL,
            name        TEXT,

            FOREIGN KEY (id_city) REFERENCES CITY (id)
        ); """,
        # use
        """CREATE TABLE IF NOT EXISTS USE (
            id_airline  INTEGER,
            id_airway   INTEGER,

            PRIMARY KEY (id_airline, id_airway),

            FOREIGN KEY (id_airline) REFERENCES AIRLINE (id),
            FOREIGN KEY (id_airway) REFERENCES AIRWAY (id)
        ); """,
        # use
        """CREATE TABLE IF NOT EXISTS FLY_ON (
            id_airway  INTEGER,
            id_plane   INTEGER,

            PRIMARY KEY (id_airway, id_plane),

            FOREIGN KEY (id_airway) REFERENCES AIRWAY (id),
            FOREIGN KEY (id_plane) REFERENCES PLANE (id)
        ); """,
        # step in
        """CREATE TABLE IF NOT EXISTS STEP_IN (
            id_airport  NUMBER,
            id_airway   NUMBER,
            rank        NUMBER,

            PRIMARY KEY (id_airport, id_airway),

            FOREIGN KEY (id_airport) REFERENCES AIRPORT (id),
            FOREIGN KEY (id_airway) REFERENCES AIRWAY (id)
        ); """
    ]
