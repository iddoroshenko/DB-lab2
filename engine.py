import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
import datetime
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

# выделенный пользователь - viktor, пароль - viktor, он подключается к существующей базе данных
# база данных создается суперпользователем db_creator


# TODO: сделать так, чтобы функции сообщали о том, что они сделали (или чего сделать не получилось)
# триггер почему-то не работает

fin = open('create_drop_func.sql')
cr_dr_func = fin.read()
fin.close()

fin = open('functions.sql')
func = fin.read()
fin.close()

engineURL = ''

def connect_as_creator(username_creator, password_creator, main_db, cr_dr_func):
    engine = create_engine(
        "postgresql+psycopg2://{}:{}@localhost/{}".format(username_creator, password_creator, main_db),
        echo=True)
    cursor = engine.connect()  # подключаемся
    cursor.execute(cr_dr_func)  # запускаем функции
    return cursor


def create_database(db_name, username,
                    cr_dr_func=cr_dr_func):  # название базы данных и имя пользователя, который будет ей пользоваться
    cursor = connect_as_creator('db_creator', 'db_creator', 'lab_db', cr_dr_func)
    cursor.execute('SELECT create_db(\'{}\', \'{}\')'.format(db_name, username))  # запускаем создание базы данных
    cursor.close()


# если в pgadmin подключаешься к базе, то от нее обязательно надо отключаться, чтобы дропалось
def drop_database(db_name, cr_dr_func=cr_dr_func):
    cursor = connect_as_creator('db_creator', 'db_creator', 'lab_db', cr_dr_func)
    cursor.execute('SELECT drop_db(\'{}\')'.format(db_name))  # запускаем удаление


def connect_as_user(username, password, db_name, functions=func):
    connection = psycopg2.connect(host='localhost', database=db_name, user=username, password=password)
    cursor = connection.cursor()
    cursor.execute(functions)
    connection.commit()
    return connection


def disconnect_user(connection):
    connection.close()


def clear_all_tables(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_all_tables()')
    connection.commit()


def clear_flower(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_flower()')
    connection.commit()


def clear_worker(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_worker()')
    connection.commit()


def clear_provider(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_provider()')
    connection.commit()


def add_to_provider(connection, in_id, in_name, in_district, in_discount):
    cursor = connection.cursor()
    cursor.execute('SELECT add_to_provider({}, \'{}\', \'{}\', {})'.format(in_id, in_name, in_district, in_discount))
    connection.commit()


def add_to_worker(connection, in_id, in_name, in_address, in_payment):
    cursor = connection.cursor()
    cursor.execute('SELECT add_to_worker({}, \'{}\', \'{}\', {})'.format(in_id, in_name, in_address, in_payment))
    connection.commit()


def add_to_flower(connection, in_id, in_name, in_provider, in_date, in_color, in_worker,
                  in_amount, in_value):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT add_to_flower({}, \'{}\', {}, \'{}\', \'{}\', {}, {}, {})'.format(in_id, in_name, in_provider, in_date,
                                                                                  in_color, in_worker,
                                                                                  in_amount, in_value))
    connection.commit()


def search_flower_by_name(connection, flower_name):
    cursor = connection.cursor()
    cursor.execute('SELECT search_flower_by_name(\'{}\')'.format(flower_name))
    table = cursor.fetchall()
    return table


def update_flower(connection, in_id, in_name, in_provider, in_date, in_color, in_worker,
                  in_amount, in_value):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT update_flower({}, \'{}\', {}, \'{}\', \'{}\', {}, {}, {})'.format(in_id, in_name, in_provider, in_date,
                                                                                  in_color, in_worker,
                                                                                  in_amount, in_value))
    connection.commit()


def delete_flower_by_name(connection, in_name):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_flower_by_name(\'{}\')'.format(in_name))
    connection.commit()


def delete_flower_by_id(connection, in_id):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_flower_by_id({})'.format(in_id))
    connection.commit()


def delete_provider_by_id(connection, in_id):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_provider_by_id({})'.format(in_id))
    connection.commit()


def delete_worker_by_id(connection, in_id):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_worker_by_id({})'.format(in_id))
    connection.commit()


def print_table_provider(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT print_table_provider()')
    table = cursor.fetchall()
    return table


# Черновик:
# add_to_provider(conn_u, 2,	'БАЗА ЦВЕТОВ 24', 'Ленинский', 0)
# add_to_worker(conn_u, 2,	'Илья Дорошенко',		'Автозаводский',	31000)
# add_to_flower(conn_u, 1200, 	'Роза',	2,    '2020/01/20', 'красный', 2, 10, 159)
# out = search_flower_by_name(conn_u, 'Роза')
# update_flower(conn_u, 127, 'Цк', -1, '2020/01/20', ' ', 2, 15, 200)
# clear_provider(conn_u)


# --- Создание базы данных ---
#create_database('new', 'viktor', cr_dr_func)

# --- удаление базы данных ---
# disconnect_user(conn_u) # обязательно нужно дисконнектить пользователя перед удалением базы (и отключаться в pgadmin)
# drop_database('new', cr_dr_func)

#conn_u = connect_as_user('viktor', 'viktor', 'new', func)  # коннектимся к базе как юзер, функция возвращает connection
# add_to_provider(conn_u, 2, 'БАЗА ЦВЕТОВ 24', 'Ленинский',
#                0)  # объект connection используется для всех функций работы с бд
# add_to_worker(conn_u, 2, 'Илья Дорошенко', 'Автозаводский', 31000)
# add_to_flower(conn_u, 1201, 'Роза', 2, '2020/01/20', 'красный', 2, 10, 159)
# update_flower(conn_u, 1200, 'Хризантема', -1, '2020/01/20', ' ', 2, 15, 280)

# delete_flower_by_name(conn_u, 'Хризантема')
