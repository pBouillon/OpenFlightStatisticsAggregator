CREATE TABLE FLY_ON
(
    id_airway	NUMBER  NOT NULL,
    id_plane	NUMBER	NOT NULL,

    CONSTRAINT PK_FLY_ON PRIMARY KEY (id_airway, id_plane),

    CONSTRAINT FK_AIRWAY
        FOREIGN KEY (id_airway)
        REFERENCES  AIRWAY(id),

    CONSTRAINT FK_PLANE
		FOREIGN KEY (id_plane)
		REFERENCES  PLANE(id)
)