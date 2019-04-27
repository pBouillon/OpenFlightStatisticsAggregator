CREATE TABLE STEP_IN
(
    id_airport	NUMBER  NOT NULL,
    id_airway	NUMBER	NOT NULL,
    rank        NUMBER  NOT NULL,

    CONSTRAINT PK_STEP_IN PRIMARY KEY (id_airport, id_airway),

    CONSTRAINT FK_AIRPORT
        FOREIGN KEY (id_airport)
        REFERENCES  AIRPORT(id),

    CONSTRAINT FK_AIRWAY
        FOREIGN KEY (id_airway)
        REFERENCES  AIRWAY(id)
)