CREATE TABLE AIRLINE
(
    id          NUMBER          NOT NULL,
    id_country  NUMBER          NOT NULL,
    active      CHAR(1)         NOT NULL,
    alias       VARCHAR2(50),
    callsing    VARCHAR2(50)    NOT NULL,
    name        VARCHAR2(100)   NOT NULL,
    iata_code   VARCHAR2(2),
    icao_code   VARCHAR2(3),

    CONSTRAINT PK_AIRLINE PRIMARY KEY (id),

    CONSTRAINT FK_COUNTRY
        FOREIGN KEY (id_country)
        REFERENCES  COUNTRY(id)
)