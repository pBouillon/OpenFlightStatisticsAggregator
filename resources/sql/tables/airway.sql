CREATE TABLE AIRWAY
(
    id              NUMBER  NOT NULL,
    id_airline      NUMBER,
    id_airport_dest NUMBER,
    id_airport_src  NUMBER,
    id_plane_type   NUMBER  NOT NULL,
    stops           NUMBER  NOT NULL,

    CONSTRAINT PK_AIRWAY PRIMARY KEY (id),

    CONSTRAINT FK_AIRLINE
        FOREIGN KEY (id_airline)
        REFERENCES  AIRLINE(id),

    CONSTRAINT FK_AIRPORT
        FOREIGN KEY (id_airport_dest)
        REFERENCES  AIRPORT(id),

    CONSTRAINT FK_AIRPORT
        FOREIGN KEY (id_airport_src)
        REFERENCES  AIRPORT(id)

    CONSTRAINT FK_PLANE_TYPE
        FOREIGN KEY (id_plane_type)
        REFERENCES  PLANE_TYPE(id),
)