CREATE TABLE IF NOT EXISTS COUNTRY (
    id          INTEGER     PRIMARY KEY,
    id_dst      INTEGER,
    name        TEXT,
    area        REAL,
    population  INTEGER,

    FOREIGN KEY (id_dst) 
        REFERENCES DST (id)
);