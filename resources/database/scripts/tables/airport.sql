CREATE TABLE AIRPORT
(
    id          NUMBER          NOT NULL,
    id_city     NUMBER          NOT NULL,
    altitude    BINARY_FLOAT	NOT NULL,
    id_iata     VARCHAR2(3),
    id_icao     VARCHAR2(4),
    latitude    BINARY_FLOAT	NOT NULL,
    longitude   BINARY_FLOAT	NOT NULL,
    name        VARCHAR2(150)	NOT NULL,

    CONSTRAINT PK_AIRPORT PRIMARY KEY (id),

    CONSTRAINT FK_CITY
        FOREIGN KEY (id_city)
        REFERENCES  CITY(id)
)