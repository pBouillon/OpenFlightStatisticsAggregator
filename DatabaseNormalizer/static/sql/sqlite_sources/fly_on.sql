CREATE TABLE IF NOT EXISTS FLY_ON (
    id_airway  INTEGER,
    id_plane   INTEGER,

    PRIMARY KEY (id_airway, id_plane),

    FOREIGN KEY 
        (id_airway) REFERENCES AIRWAY (id),
        
    FOREIGN KEY (id_plane) 
        REFERENCES PLANE (id)
);
