CREATE TABLE USE
(
    id_airline	NUMBER  NOT NULL,
    id_airway	NUMBER	NOT NULL,

    CONSTRAINT PK_USE PRIMARY KEY (id_airline, id_airway),

    CONSTRAINT FK_AIRLINE
        FOREIGN KEY (id_airline)
        REFERENCES  AIRPORT(id),

    CONSTRAINT FK_AIRWAY
        FOREIGN KEY (id_airway)
        REFERENCES  AIRWAY(id)
)