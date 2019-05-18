CREATE TABLE IF NOT EXISTS PLANE (
    id              INTEGER     PRIMARY KEY,
    id_plane_type   INTEGER,
    iata_code       TEXT,
    icao_code       TEXT,
    model           TEXT,
    passengers      INTEGER,
    consumption     INTEGER,
    freight         INTEGER,
    speed           INTEGER,

    FOREIGN KEY (id_plane_type) 
        REFERENCES PLANE_TYPE(id)
);
