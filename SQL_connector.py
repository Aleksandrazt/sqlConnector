import mysql.connector
import sqlite3
import psycopg2
import pandas as pd
from known_databases_conf import ALL_POSSIBLE_CONFIGS, DB_TYPES


def get_data_from_db(request: str, db: str, head: list):
    """
    Connect to database and get information
    :param head: names for DataFrame
    :param request: sql request as str
    :param db: name of database as str
    :return: result of request as list
    """
    if DB_TYPES[db] == 'mysql':
        cnx = mysql.connector.connect(**ALL_POSSIBLE_CONFIGS[db])
    elif DB_TYPES[db] == 'sqlite':
        cnx = sqlite3.connect(ALL_POSSIBLE_CONFIGS[db])  # path to db in dict
    else:
        cnx = psycopg2.connect(**ALL_POSSIBLE_CONFIGS[db])  # database, user, password, host, port
    cursor = cnx.cursor()
    cursor.execute(request)
    result = cursor.fetchall()
    cnx.close()
    result = pd.DataFrame(result)
    pd.set_option('display.max_columns', 6)
    pd.options.display.expand_frame_repr = False
    if not result.empty and head:
        result.columns = head
    return result
