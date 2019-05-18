CREATE TABLE PLANE_TYPE
(
    id          NUMBER          NOT NULL,
    iata_code     VARCHAR2(3)     NOT NULL,
    type        VARCHAR2(30)	NOT NULL,

    CONSTRAINT PK_PLANE_TYPE PRIMARY KEY (id)
)