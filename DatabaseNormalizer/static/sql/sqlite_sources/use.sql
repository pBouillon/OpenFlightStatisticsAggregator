CREATE TABLE IF NOT EXISTS USE (
    id_airline  INTEGER,
    id_airway   INTEGER,

    PRIMARY KEY (id_airline, id_airway),

    FOREIGN KEY (id_airline) 
        REFERENCES AIRLINE (id),
        
    FOREIGN KEY (id_airway) 
        REFERENCES AIRWAY (id)
);