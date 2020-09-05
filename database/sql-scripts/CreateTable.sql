
CREATE TABLE users ( id MEDIUMINT NOT NULL AUTO_INCREMENT, email varchar (25) NOT NULL, username varchar (50), password varchar (50), first_name varchar (50), last_name varchar (50), role varchar (8) DEFAULT 'User', PRIMARY KEY (id));

