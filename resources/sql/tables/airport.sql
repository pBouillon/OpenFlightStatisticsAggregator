CREATE TABLE AIRPORT
(
    id          NUMBER          NOT NULL,
    id_city     NUMBER          NOT NULL,
    altitude    BINARY_FLOAT    NOT NULL,
    latitude    BINARY_FLOAT    NOT NULL,
    longitude   BINARY_FLOAT    NOT NULL,
    name        VARCHAR(150)    NOT NULL,
    id_iata     VARCHAR(3),
    id_icao     VARCHAR(4),

    CONSTRAINT PK_AIRPORT PRIMARY KEY (id),

    CONSTRAINT FK_CITY
        FOREIGN KEY (id_city)
        REFERENCES  CITY(id)
)