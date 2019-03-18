CREATE TABLE COUNTRY 
(  
    id			NUMBER,  
    id_dst		NUMBER,  
    name		VARCHAR(50),  
    inhabitants	NUMBER,  
    superficy	BINARY_FLOAT,
  
    CONSTRAINT FK_COUNTRY_DST  
    FOREIGN KEY (id_dst) REFERENCES DST (id),  
    CONSTRAINT PK_COUNTRY PRIMARY KEY (id)
)