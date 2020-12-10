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
	totalCost INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (provider) REFERENCES Provider(id) ON DELETE CASCADE,
	FOREIGN KEY (worker) REFERENCES Worker(id) ON DELETE CASCADE
);

CREATE INDEX name ON Flower (name);

INSERT INTO Provider (id, name, district, discount)
VALUES
(001,	'БАЗА ЦВЕТОВ 24',		'Ленинский',		0),
(002,	'ФлорАрт',				'Ленинский',		20),
(003,	'Радуга',				'Советский',		5),
(004,	'Букет',				'Дзержинск',		5),
(005,	'Азалия',				'Советский',		7),
(006,	'Упаковка 52',			'Канавинский',		10),
(007,	'APRIL cash & carry',	'Советский',		0),
(008,	'Цветочек 1000',		'Нижегородский',	15),
(009,	'Флора',				'Ленинский',		25);

INSERT INTO Worker (id, name, address, payment)
VALUES
(001,	'Илья Дорошенко',		'Автозаводский',	30000),
(002,	'Евгений Мельников',	'Ленинский',		35000),
(003,	'Андрей Носков',		'Сормовский',		25000),
(004,	'Алина Соловьева',		'Автозаводский',	19000),
(005,	'Александра Вохмянина',	'Кстово',			40000),
(006,	'Козлова Оксана',		'Сормовский',		15000);

INSERT INTO Flower (id, name, provider, date, color, worker, amount, value)
VALUES 
(00127, 	'Пуансеттия 30 см',							003,    to_date('2020/01/20','YYYY/MM/DD'),		'красный',		001,	10,	159),
(00128, 	'Орхидея Фалееопсис 1 ствол',				002,	to_date('2020/02/22','YYYY/MM/DD'),		'желтый',		002,	15,	699),
(00129, 	'Орхидея Фаленопсис Элегант Дебора',		001, 	to_date('2020/03/15','YYYY/MM/DD'),		'фиолетовый',	002,	5,	1899),
(00130, 	'Орхидея Фаленопсис оптифлор мультифлор',	009,	to_date('2020/04/02','YYYY/MM/DD'),		'белый',		002,	5,	1699),
(00131, 	'Орхидея Фаленопсис Роял Блю',				007,	to_date('2020/04/01','YYYY/MM/DD'),		'голубой',		005,	5,	1299),
(00132, 	'Пуансеттия 60 см',							005, 	to_date('2020/04/05','YYYY/MM/DD'),		'красный',		001,	7,	599),
(00133, 	'Бегония Элатиор',							004,	to_date('2020/05/12','YYYY/MM/DD'),		'розовый',		001,	25,	369),
(00134, 	'Каланхое Каландива',						008,	to_date('2020/05/30','YYYY/MM/DD'),		'оранжевый',	001,	9,	199),
(00135, 	'Фикус Гинсенг',							006,	to_date('2020/05/03','YYYY/MM/DD'),		'зеленый',		006,	6,	1299),
(00136, 	'Бегония Мэйсона',							009,	to_date('2020/06/05','YYYY/MM/DD'),		'зеленый',		001,	15,	149),
(00137, 	'Хавортия Микс',							009,	to_date('2020/06/29','YYYY/MM/DD'),		'зеленый',		003,	3,	299),
(00138, 	'Каллизия ползучая',						005,	to_date('2020/06/30','YYYY/MM/DD'),		'зеленый',		003,	17,	129),
(00139, 	'Кактус Мамиллярия',						008,	to_date('2020/06/30','YYYY/MM/DD'),		'желтый',		005,	35,	369),
(00140, 	'Плющ',										009,	to_date('2020/06/30','YYYY/MM/DD'),		'зеленый',		001,	10,	299),
(00141, 	'Эхеверия Мэджик',							001,	to_date('2020/06/30','YYYY/MM/DD'),		'зеленый',		005,	3,	499),
(00142, 	'Хавортия мороз',							002,	to_date('2020/07/07','YYYY/MM/DD'),		'белый',		006,	2,	529),
(00143, 	'Крассула Овата',							003,	to_date('2020/09/10','YYYY/MM/DD'),		'зеленый',		004,	5,	1699);
(00143, 	'Хавортия',									003,	to_date('2020/09/10','YYYY/MM/DD'),		'красный',		001,	6,	399);
