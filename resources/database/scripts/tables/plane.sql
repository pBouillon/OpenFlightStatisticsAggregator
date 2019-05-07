CREATE TABLE PLANE
(
    id              NUMBER          NOT NULL,
    id_plane_type   NUMBER          NOT NULL,
    consumption     NUMBER,
    freight         NUMBER,
    iata_code       VARCHAR2(3),
    icao_code       VARCHAR2(4)		NOT NULL,
    model           VARCHAR2(30)	NOT NULL,
    passengers      NUMBER,
    speed           NUMBER,

    CONSTRAINT PK_PLANE PRIMARY KEY (id),

    CONSTRAINT FK_PLANE_TYPE
        FOREIGN KEY (id_plane_type)
        REFERENCES  PLANE_TYPE(id)
)