import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

db_config = {
    'host' : '127.0.0.1',
    'port' : 3306,
    'user' : 'root',
    'password' : os.getenv("MYSQL_ROOT_PASS"),
    'database' : 'test'
}

tables_config = {
    'exchange_rates' : {
        'table_name' : 'exchange_rates',
        'field_names' : ('currency', 'timestamp', 'rate'),
        'field_type' : ('VARCHAR(255)','TIMESTAMP','DOUBLE')
    }
}

cnx = mysql.connector.connect(** db_config)
cursor = cnx.cursor()

file_open = open('utils/insert_data.sql', 'r')
str_query = file_open.read()

def build_insert_query(
    table_name : str,
):
    field_names = str(tables_config[table_name]['field_names']).replace("'","")
    replacement_values = '(%s'+str( (len(tables_config[table_name]['field_names']) - 1) * ',%s')+')'
    format_str_query = str_query.format(table_name = table_name, field_names = field_names, replacement_values = replacement_values)
    return format_str_query

rates_insert_values = ('BTC',datetime.now(),20543.226)
cursor.execute(build_insert_query('exchange_rates'), rates_insert_values)

cnx.commit()
