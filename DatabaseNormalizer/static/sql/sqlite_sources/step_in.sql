CREATE TABLE IF NOT EXISTS STEP_IN (
    id          NUMBER      PRIMARY KEY, 
    id_airport  NUMBER,
    id_airway   NUMBER,
    rank        NUMBER,

    FOREIGN KEY (id_airport) 
        REFERENCES AIRPORT (id),
    FOREIGN KEY (id_airway) 
        REFERENCES AIRWAY (id)
);
