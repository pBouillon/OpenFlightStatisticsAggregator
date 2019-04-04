CREATE TABLE COUNTRY 
(
	id          NUMBER          NOT NULL,
	id_dst      NUMBER          NOT NULL,
	inhabitants NUMBER,
	name        VARCHAR2(50)    NOT NULL,
	superficy   BINARY_FLOAT,

	CONSTRAINT PK_COUNTRY PRIMARY KEY (id)
	
  	CONSTRAINT FK_COUNTRY_DST
		FOREIGN KEY (id_dst)
		REFERENCES DST (id),
)