CREATE TABLE PLANE_TYPE
(
    id          NUMBER  	NOT NULL,
    type        VARCHAR(50)	NOT NULL,
    consumption NUMBER,
    freight     NUMBER,
    id_iata     VARCHAR(3),
    id_icao     VARCHAR(4),
    passengers  NUMBER,
    speed       NUMBER,

    CONSTRAINT PK_PLANE_TYPE PRIMARY KEY (id),
)