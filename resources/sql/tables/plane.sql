CREATE TABLE PLANE
(
    id              NUMBER  NOT NULL,
    id_airline      NUMBER  NOT NULL,
    id_plane_type   NUMBER  NOT NULL,
    id_iata         NUMBER  NOT NULL,
    id_icao         NUMBER  NOT NULL,

    CONSTRAINT PK_ICAO PRIMARY KEY (id),

    CONSTRAINT FK_AIRLINE
        FOREIGN KEY (id_airline)
        REFERENCES  AIRLINE(id),

    CONSTRAINT FK_PLANE_TYPE
        FOREIGN KEY (id_plane_type)
        REFERENCES  PLANE_TYPE(id),

    CONSTRAINT FK_IATA
        FOREIGN KEY (id_iata)
        REFERENCES  IATA(id),

    CONSTRAINT FK_ICAO
        FOREIGN KEY (id_icao)
        REFERENCES  ICAO(id)
)