CREATE TABLE PLANE
(
    id          	NUMBER  	NOT NULL,
    id_plane_type   NUMBER,
    name        	VARCHAR(50)	NOT NULL,
    consumption 	NUMBER,
    freight     	NUMBER,
    id_iata     	VARCHAR(3),
    id_icao     	VARCHAR(4)	NOT NULL,
    passengers  	NUMBER,
    speed       	NUMBER,

    CONSTRAINT PK_PLANE PRIMARY KEY (id),

    CONSTRAINT FK_PLANE_TYPE
        FOREIGN KEY (id_plane_type)
        REFERENCES  PLANE_TYPE(id)
)