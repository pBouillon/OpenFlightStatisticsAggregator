CREATE TABLE AIRLINE
(
    id          NUMBER          NOT NULL,
    id_country  NUMBER          NOT NULL,
    active      BOOLEAN         NOT NULL,
    alias       VARCHAR2(50),
    callsing    VARCHAR2(50)    NOT NULL,
    name        VARCHAR2(100)   NOT NULL,
    id_iata     VARCHAR2(2),
    id_icao     VARCHAR2(3),

    CONSTRAINT PK_AIRLINE PRIMARY KEY (id),

    CONSTRAINT FK_COUNTRY
        FOREIGN KEY (id_country)
        REFERENCES  COUNTRY(id)
)