-- TODO: 
-- Стоит во всех функциях добавить return 1 при успешном выполнении и return 0 или -1, если по какой-то причине действие нельзя исполнить 
-- Обновление кортежа
-- выделенный пользователь

-- [4]
-- очистка всех таблиц
DROP FUNCTION IF EXISTS clear_all_tables();
CREATE FUNCTION clear_all_tables()
	RETURNS void AS 
	$$ 
	DELETE FROM flower;
	DELETE FROM provider;
	DELETE FROM worker;
	$$
	
LANGUAGE sql;


-- очистка таблицы flower
DROP FUNCTION IF EXISTS clear_flower();
CREATE FUNCTION clear_flower()
	RETURNS void AS 
	$$ 
	DELETE FROM flower;
	$$	
LANGUAGE sql;


-- очистка таблицы worker
DROP FUNCTION IF EXISTS clear_worker();
CREATE FUNCTION clear_worker()
	RETURNS void AS 
	$$ 
	DELETE FROM worker;
	$$	
LANGUAGE sql;


-- очистка таблицы provider
DROP FUNCTION IF EXISTS clear_provider();
CREATE FUNCTION clear_provider()
	RETURNS void AS 
	$$ 
	DELETE FROM provider;
	$$	
LANGUAGE sql;


-- [5]
-- добавление provider в таблицу
DROP FUNCTION IF EXISTS add_to_provider(INTEGER, VARCHAR(40), VARCHAR(20), INTEGER);
CREATE FUNCTION add_to_provider(in_id INTEGER, in_name VARCHAR(40), in_district VARCHAR(20), in_discount INTEGER) -- in означает input
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT p.id FROM provider p WHERE p.id = in_id) THEN
			RAISE NOTICE 'Provider with id % already exists', in_id;
			RETURN 0;
		ELSE 
			INSERT INTO Provider (id, name, district, discount)
			VALUES (in_id, in_name, in_district, in_discount);
			RETURN 1;
		END IF;
	END;
	$$ LANGUAGE plpgsql;


-- добавление worker в таблицу
DROP FUNCTION IF EXISTS add_to_worker(INTEGER, VARCHAR(40), VARCHAR(20), INTEGER);
CREATE FUNCTION add_to_worker(in_id INTEGER, in_name VARCHAR(40), in_address VARCHAR(20), in_payment INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT w.id FROM worker w WHERE w.id = in_id) THEN
			RAISE NOTICE 'Worker with id % already exists', in_id;
			RETURN 0;
		ELSE 
			INSERT INTO Worker (id, name, address, payment)
			VALUES (in_id, in_name, in_address, in_payment);
			RETURN 1;
		END IF;
	END;
	$$ LANGUAGE plpgsql;


-- добавление flower в таблицу
DROP FUNCTION IF EXISTS add_to_flower(INTEGER, VARCHAR(40), INTEGER, VARCHAR(20), INTEGER, INTEGER, INTEGER);
CREATE FUNCTION add_to_flower(in_id INTEGER, in_name VARCHAR(40), in_provider INTEGER, in_color VARCHAR(20), in_worker INTEGER,
							  in_amount INTEGER, in_value INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF NOT EXISTS (SELECT p.id FROM provider p WHERE p.id = in_provider) THEN
			RAISE NOTICE 'Provider % does not exist', in_provider;
			RETURN 0;
		
		ELSIF NOT EXISTS (SELECT w.id FROM worker w WHERE w.id = in_worker) THEN
			RAISE NOTICE 'Worker % does not exist', in_worker;
			RETURN 0;						  
		ELSIF EXISTS (SELECT f.id FROM flower f WHERE f.id = in_id) THEN
			RAISE NOTICE 'Flower with id % already exists', in_id;
			RETURN 0;
		ELSE
			INSERT INTO flower (id, name, provider, color, worker, amount, value)
			VALUES (in_id, in_name, in_provider, in_color, in_worker, in_amount, in_value);
			RETURN 1;
		END IF;
	END;
	$$ LANGUAGE plpgsql;


-- [6]
-- поиск по названию цветка
DROP FUNCTION IF EXISTS search_flower_by_name(VARCHAR(40));
CREATE FUNCTION search_flower_by_name(in_name VARCHAR(40))
	RETURNS TABLE (id INTEGER,	name VARCHAR(40), provider INTEGER ,color VARCHAR(20), worker INTEGER, amount INTEGER, value INTEGER, totalCost INTEGER) AS
	$$
	BEGIN 
		IF EXISTS (SELECT f.name FROM flower f WHERE f.name = in_name) THEN
			RETURN QUERY
				SELECT * FROM flower f
				WHERE f.name=in_name;
		ELSE 
			RAISE NOTICE 'Flower with name % does not exist', in_name;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


-- [7]
-- обновление записи в таблице flower по id 
-- если на вход вместо числа подается -1 или если вместо строки подается '', этот аттрибут остается без изменения
DROP FUNCTION IF EXISTS update_flower(INTEGER, VARCHAR(40), INTEGER, VARCHAR(20), INTEGER, INTEGER, INTEGER);
CREATE FUNCTION update_flower(in_id INTEGER, in_name VARCHAR(40), in_provider INTEGER, in_color VARCHAR(20), in_worker INTEGER,
							  in_amount INTEGER, in_value INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT f.id FROM flower f WHERE f.id = in_id) THEN
			IF (in_provider <> -1) AND NOT EXISTS (SELECT p.id FROM provider p WHERE p.id = in_provider) THEN
				RAISE NOTICE 'Provider % does not exist', in_provider;
				RETURN 0;
		
			ELSIF (in_worker <> -1) AND NOT EXISTS (SELECT w.id FROM worker w WHERE w.id = in_worker) THEN
				RAISE NOTICE 'Worker % does not exist', in_worker;
				RETURN 0;
			ELSE
				IF (in_name <> '') THEN
					UPDATE flower f
					SET name = in_name
					WHERE id = in_id;
				END IF;
				IF (in_provider <> -1) THEN 
					UPDATE flower 
					SET provider = in_provider
					WHERE id = in_id;
				END IF;
				IF (in_color <> '') THEN
					UPDATE flower 
					SET color = in_color
					WHERE id = in_id;
				END IF;
				IF (in_worker <> -1) THEN 
					UPDATE flower 
					SET worker = in_worker
					WHERE id = in_id;
				END IF;
				IF (in_amount <> -1) THEN 
					UPDATE flower 
					SET amount = in_amount
					WHERE id = in_id;
				END IF;
				IF (in_value <> -1) THEN 
					UPDATE flower 
					SET value = in_value
					WHERE id = in_id;
				END IF;
				RETURN 1;
			END IF;
		ELSE 
			RAISE NOTICE 'Flower with id % does not exist', in_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;



--[8]
-- удаление цветков по названию
DROP FUNCTION IF EXISTS delete_flower_by_name(VARCHAR(40));
CREATE FUNCTION delete_flower_by_name(in_name VARCHAR(40))
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT f.name FROM flower f WHERE f.name = in_name) THEN
			DELETE FROM flower f
			WHERE f.name = in_name;
			RETURN 1;
		ELSE 
			RAISE NOTICE 'Flower with name % does not exist', in_name;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


-- [9]
-- удаление цветков по айди
DROP FUNCTION IF EXISTS delete_flower_by_id(INTEGER);
CREATE FUNCTION delete_flower_by_id(in_id INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT f.id FROM flower f WHERE f.id = in_id) THEN
			DELETE FROM flower f
			WHERE f.id = in_id;
			RETURN 1;
		ELSE 
			RAISE NOTICE 'Flower with id % does not exist', in_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


-- удаленние поставщика по айди
DROP FUNCTION IF EXISTS delete_provider_by_id(INTEGER);
CREATE FUNCTION delete_provider_by_id(in_id INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT p.id FROM provider p WHERE p.id = in_id) THEN
			DELETE FROM provider p
			WHERE p.id = in_id;
			RETURN 1;
		ELSE 
			RAISE NOTICE 'Provider with id % does not exist', in_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


-- удаление работника по айди
DROP FUNCTION IF EXISTS delete_worker_by_id(INTEGER);
CREATE FUNCTION delete_worker_by_id(in_id INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN 
		IF EXISTS (SELECT w.id FROM worker w WHERE w.id = in_id) THEN
			DELETE FROM worker w
			WHERE w.id = in_id;
			RETURN 1;
		ELSE 
			RAISE NOTICE 'Worker with id % does not exist', in_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;

-- вывод таблицы цветов
DROP FUNCTION IF EXISTS print_table_flower();
CREATE FUNCTION print_table_flower()
	RETURNS TABLE (id INTEGER,	name VARCHAR(40), provider INTEGER ,	color VARCHAR(20), worker INTEGER, amount INTEGER, value INTEGER, totalCost INTEGER) AS
	$$
	BEGIN
		IF EXISTS (SELECT * FROM flower) THEN
			RETURN QUERY
				SELECT * FROM flower;
		ELSE
			RAISE NOTICE 'Table is empty';
		END IF;
	END;
	$$
LANGUAGE plpgsql;

-- вывод таблицы поставщиков
DROP FUNCTION IF EXISTS print_table_provider();
CREATE FUNCTION print_table_provider()
	RETURNS TABLE (id INTEGER,	name VARCHAR(40), district VARCHAR(20), discount INTEGER) AS
	$$
	BEGIN
		IF EXISTS (SELECT * FROM provider) THEN
			RETURN QUERY
				SELECT * FROM provider;
		ELSE
			RAISE NOTICE 'Table is empty';
		END IF;
	END;
	$$
LANGUAGE plpgsql;

-- вывод таблицы работников
DROP FUNCTION IF EXISTS print_table_worker();
CREATE FUNCTION print_table_worker()
	RETURNS TABLE (id INTEGER,	name VARCHAR(40), address VARCHAR(20), payment INTEGER) AS
	$$
	BEGIN
		IF EXISTS (SELECT * FROM worker) THEN
			RETURN QUERY
				SELECT * FROM worker;
		ELSE
			RAISE NOTICE 'Table is empty';
		END IF;
	END;
	$$
LANGUAGE plpgsql;