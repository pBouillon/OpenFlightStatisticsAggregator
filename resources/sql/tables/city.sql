CREATE TABLE CITY
(
    id          NUMBER          NOT NULL,
    id_country  NUMBER          NOT NULL,
    id_timezone NUMBER          NOT NULL,
    name        VARCHAR(100)    NOT NULL,

    CONSTRAINT PK_CITY PRIMARY KEY (id),

    CONSTRAINT FK_COUNTRY
        FOREIGN KEY (id_country)
        REFERENCES  COUNTRY(id),

    CONSTRAINT FK_TIMEZONE
        FOREIGN KEY (id_timezone)
        REFERENCES  TIMEZONE(id)
)