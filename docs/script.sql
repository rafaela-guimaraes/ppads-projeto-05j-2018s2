CREATE TABLE CATEGORY (
	id				INT	 IDENTITY PRIMARY KEY,
	entries_type	CHAR(2)	NOT NULL,
	description		VARCHAR(100) NOT NULL,
);
CREATE TABLE USERS (
	id INT NOT NULL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	email VARCHAR(100) NOT NULL,
);

CREATE TABLE ENTRY(
	id INT PRIMARY KEY,
	category_id INT NOT NULL,
	userid INT NOT NULL,
	description VARCHAR(100) NOT NULL,
	amount DECIMAL(18,2) NOT NULL, 
	entry_date DATE NOT NULL, 
	
	CONSTRAINT fk_category_entry
    FOREIGN KEY (category_id)
    REFERENCES CATEGORY(id),
	
	CONSTRAINT fk_user_entry
    FOREIGN KEY (userid)
    REFERENCES USERS(id),
	
)