CREATE TABLE AIRLINE
(
    id          NUMBER          NOT NULL,
    id_country  NUMBER          NOT NULL,
    active      BOOLEAN         NOT NULL,
    alias       VARCHAR(50),
    callsing    VARCHAR(50)     NOT NULL,
    name        VARCHAR(100)    NOT NULL,

    CONSTRAINT PK_AIRLINE PRIMARY KEY (id),

    CONSTRAINT FK_COUNTRY
        FOREIGN KEY (id_country)
        REFERENCES  COUNTRY(id)
)