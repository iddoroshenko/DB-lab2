CREATE EXTENSION IF NOT EXISTS dblink; -- чтобы иметь возможность создавать базы данных внутри функции
-- dblink позволяет делать запросы у "удаленным" базам данных

DROP FUNCTION IF EXISTS create_db(text, text); 
CREATE FUNCTION create_db(dbname text, username text)
	RETURNS INTEGER AS
	$func$
	BEGIN
		IF EXISTS (SELECT datname FROM pg_database WHERE datname = dbname) THEN
   			RAISE NOTICE 'Database "%%" already exists', dbname;
			RETURN 0; 
		ELSE
   			PERFORM dblink_exec('user=db_creator password=db_creator dbname=' || current_database(),
								'CREATE DATABASE ' || dbname); 
								
			PERFORM dblink_exec('user=db_creator password=db_creator dbname=' || dbname,
				'DROP TABLE IF EXISTS Provider CASCADE;
				CREATE TABLE Provider(
					id INTEGER NOT NULL UNIQUE,
					name VARCHAR(40) NOT NULL,
					district VARCHAR(20) NOT NULL,
					discount INTEGER NOT NULL DEFAULT 0,
					PRIMARY KEY (id)
				);

				DROP TABLE IF EXISTS Worker CASCADE;
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
					color VARCHAR(20) NOT NULL,
					worker INTEGER NOT NULL,
					amount INTEGER NOT NULL,
					value INTEGER NOT NULL,
					totalCost INTEGER,
					PRIMARY KEY (id),
					FOREIGN KEY (provider) REFERENCES Provider(id) ON DELETE CASCADE,
					FOREIGN KEY (worker) REFERENCES Worker(id) ON DELETE CASCADE
				);

				CREATE INDEX name ON Flower (name);

				DROP FUNCTION IF EXISTS update_totalCost() CASCADE;
				CREATE OR REPLACE FUNCTION update_totalCost() 
				RETURNS TRIGGER AS 
				$$
				BEGIN	
					NEW.totalCost = NEW.amount*NEW.value;
					RETURN NEW; 
				END;
				$$ 
				LANGUAGE plpgsql;

				DROP TRIGGER IF EXISTS update_totalCost on Flower;
				CREATE TRIGGER update_totalCost BEFORE INSERT OR UPDATE ON Flower
				FOR EACH ROW EXECUTE PROCEDURE update_totalCost();
				'
			);

			PERFORM dblink_exec('user=db_creator password=db_creator dbname=' || dbname,
			'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ' || username );
			RETURN 1;
		END IF;

	END
	$func$ 
	LANGUAGE plpgsql;


-- [2]
-- удаление базы данных по имени 
DROP FUNCTION IF EXISTS drop_db(text);
CREATE FUNCTION drop_db(dbname text)
	RETURNS INTEGER AS
	$func$
	BEGIN
		IF EXISTS (SELECT datname FROM pg_database WHERE datname = dbname) THEN
   			PERFORM dblink_exec('user=db_creator password=db_creator dbname=' || current_database(), 
								'DROP DATABASE ' || quote_ident(dbname));
			RETURN 1;			
		ELSE
			RAISE NOTICE 'Database "%%" does not exist', dbname;
			RETURN 0; 
		END IF;

	END
	$func$ 
	LANGUAGE plpgsql;

