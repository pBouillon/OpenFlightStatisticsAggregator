CREATE TABLE COUNTRY 
(
	id		NUMBER,
	id_dst		NUMBER,
	name		VARCHAR(50),
	inhabitants	NUMBER,
	superficy	BINARY_FLOAT,

	CONSTRAINT PK_COUNTRY PRIMARY KEY (id)
	
  	CONSTRAINT FK_COUNTRY_DST
		FOREIGN KEY (id_dst)
		REFERENCES DST (id),
)