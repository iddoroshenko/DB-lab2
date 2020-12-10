DROP TABLE IF EXISTS Provider;
CREATE TABLE Provider(
	id INTEGER NOT NULL UNIQUE,
	name VARCHAR(40) NOT NULL,
	district VARCHAR(20) NOT NULL,
	discount INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY (id)
);

DROP TABLE IF EXISTS Worker;
CREATE TABLE Worker(
	id INTEGER NOT NULL UNIQUE,
	name VARCHAR(40) NOT NULL,
	address VARCHAR(20) NOT NULL,
	payment INTEGER NOT NULL,
	PRIMARY KEY (id)
);

DROP TABLE IF EXISTS Flower;
CREATE TABLE Flower(
	id INTEGER NOT NULL UNIQUE,
	name VARCHAR(40) NOT NULL,
	provider INTEGER NOT NULL,
	date DATE NOT NULL,
	color VARCHAR(20) NOT NULL,
	worker INTEGER NOT NULL,
	amount INTEGER NOT NULL,
	value INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (provider) REFERENCES Provider(id) ON DELETE CASCADE,
	FOREIGN KEY (worker) REFERENCES Worker(id) ON DELETE CASCADE
);

