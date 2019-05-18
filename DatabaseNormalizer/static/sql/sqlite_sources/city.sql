CREATE TABLE IF NOT EXISTS CITY (
    id          INTEGER     PRIMARY KEY, 
    id_country  INTEGER, 
    id_timezone INTEGER, 
    name        TEXT,
    population  INTEGER, 

    FOREIGN KEY (id_country) 
        REFERENCES COUNTRY (id),

    FOREIGN KEY (id_timezone) 
        REFERENCES TIMEZONE (id)
);
