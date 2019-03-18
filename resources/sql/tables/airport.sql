CREATE TABLE AIRPORT
(
    id          NUMBER          NOT NULL,
    id_city     NUMBER          NOT NULL,
    id_iata     NUMBER,
    id_icao     NUMBER          NOT NULL,
    altitude    BINARY_FLOAT    NOT NULL,
    latitude    BINARY_FLOAT    NOT NULL,
    longitude   BINARY_FLOAT    NOT NULL,
    name        VARCHAR(150)    NOT NULL

    CONSTRAINT PK_AIRPORT PRIMARY KEY (id),

    CONSTRAINT FK_CITY
        FOREIGN KEY (id_city)
        REFERENCES  CITY(id),

    CONSTRAINT FK_IATA
        FOREIGN KEY (id_iata)
        REFERENCES  IATA(id),

    CONSTRAINT FK_ICAO
        FOREIGN KEY (id_icao)
        REFERENCES  ICAO(id)
)