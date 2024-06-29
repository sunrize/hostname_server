CREATE TABLE [IF NOT EXISTS] hostnames (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	prefix TEXT(4) NOT NULL,
	postfix TEXT(4),
	description TEXT
);

CREATE TABLE [IF NOT EXISTS] macs (
	mac_str TEXT(17) NOT NULL,
	mac_int INTEGER NOT NULL,
	hostname_id INTEGER,
	CONSTRAINT macs_unique UNIQUE (mac_str),
	CONSTRAINT macs_pk PRIMARY KEY (mac_int),
	CONSTRAINT macs_hostname_FK FOREIGN KEY (hostname_id) REFERENCES hostnames(id) ON DELETE RESTRICT
);

CREATE TABLE [IF NOT EXISTS] descriptions (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	text TEXT NOT NULL,
	client TEXT(4) NOT NULL,
	hostname_id INTEGER NOT NULL,
	CONSTRAINT description_hostname_FK FOREIGN KEY (hostname_id) REFERENCES hostnames(id) ON DELETE RESTRICT
	CONSTRAINT description_unique UNIQUE (text,client,hostname_id)
);