CREATE TABLE PLANE_TYPE
(
    id          NUMBER  	NOT NULL,
    type        VARCHAR(50)	NOT NULL,
    consumption NUMBER,
    freight     NUMBER,
    passengers  NUMBER,
    speed       NUMBER,

    CONSTRAINT PK_PLANE_TYPE PRIMARY KEY (id),
)