CREATE TABLE AIRLINE
(
    id          NUMBER          NOT NULL,
    id_country  NUMBER          NOT NULL,
    active      BOOLEAN         NOT NULL,
    alias       VARCHAR(50),
    callsing    VARCHAR(50)     NOT NULL,
    name        VARCHAR(100)    NOT NULL,
    id_iata     VARCHAR(2),
    id_icao     VARCHAR(3),

    CONSTRAINT PK_AIRLINE PRIMARY KEY (id),

    CONSTRAINT FK_COUNTRY
        FOREIGN KEY (id_country)
        REFERENCES  COUNTRY(id)
)