CREATE TABLE PLANE_TYPE
(
    id          NUMBER          NOT NULL,
    id_iata     VARCHAR2(3)		NOT NULL,
    type        VARCHAR2(30)	NOT NULL,

    CONSTRAINT PK_PLANE_TYPE PRIMARY KEY (id)
)