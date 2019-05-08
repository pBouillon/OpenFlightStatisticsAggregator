CREATE TABLE IF NOT EXISTS AIRLINE (
    id          INTEGER     PRIMARY KEY,
    id_country  INTEGER,
    active      BOOLEAN,
    alias       TEXT,
    callsing    TEXT,
    name        TEXT,
    iata_code   TEXT,
    icao_code   TEXT,

    FOREIGN KEY (id_country) 
        REFERENCES COUNTRY (id)
);
