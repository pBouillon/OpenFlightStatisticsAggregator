CREATE TABLE PLANE_AIRWAY
(
    id              NUMBER  NOT NULL,
    id_airway       NUMBER  NOT NULL,
    id_plane_type   NUMBER  NOT NULL,

    CONSTRAINT PK_PLANE_AIRWAY PRIMARY KEY (id),

    CONSTRAINT FK_AIRWAY
        FOREIGN KEY (id_airway)
        REFERENCES  AIRWAY(id),

    CONSTRAINT FK_PLANE_TYPE
        FOREIGN KEY (id_plane_type)
        REFERENCES  PLANE_TYPE(id)
)