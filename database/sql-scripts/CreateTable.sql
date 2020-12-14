
CREATE TABLE users ( id MEDIUMINT NOT NULL AUTO_INCREMENT, email varchar (25) NOT NULL UNIQUE, username varchar (50), password varchar (50) NOT NULL, first_name varchar (50), last_name varchar (50), accept BOOLEAN DEFAULT FALSE, role varchar (8) DEFAULT 'User', PRIMARY KEY (id));

