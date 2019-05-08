CREATE TABLE IF NOT EXISTS AIRPORT (
    id          INTEGER     PRIMARY KEY,
    id_city     INTEGER,
    altitude    REAL,
    iata_code   TEXT,
    icao_code   TEXT,
    latitude    REAL,
    longitude   REAL,
    name        TEXT,

    FOREIGN KEY (id_city) 
        REFERENCES CITY (id)
);
