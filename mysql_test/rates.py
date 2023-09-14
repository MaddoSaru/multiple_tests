import pandas as pd
import mysql.connector
from datetime import datetime
import requests
from typing import Dict
from dotenv import load_dotenv
import os

load_dotenv()

currencies = [
    'BTC',
    'ETH',
]

api_key = os.getenv("CRYPTOCOMPARE_API_KEY")

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

def get_rates_df(
    currency : str
) -> pd.DataFrame:
    url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={currency}&tsym=USD&api_key={api_key}&limit=2000'
    request = requests.get(url = url).json()['Data']['Data']
    rates_df = pd.DataFrame(request)
    rates_df = rates_df[['time','close']]
    rates_df['currency'] = currency
    rates_df['time'] = pd.to_datetime(rates_df['time'], unit = 's')
    rates_df.rename(columns = {'currency':'currency', 'time':'timestamp', 'close':'rate'}, inplace = True)    
    return rates_df

def build_insert_query(
    table_name : str,
):
    field_names = str(tables_config[table_name]['field_names']).replace("'","")
    replacement_values = '(%s'+str( (len(tables_config[table_name]['field_names']) - 1) * ',%s')+')'
    format_str_query = str_query.format(table_name = table_name, field_names = field_names, replacement_values = replacement_values)
    return format_str_query

def insert_mysql_values(
    currency : str,
    table_name : str,
):
    rates_df = get_rates_df(currency)
    insert_query = build_insert_query(table_name)
    for index in rates_df.index:
        rates_insert_values = (rates_df['currency'][index], rates_df['timestamp'][index], rates_df['rate'][index])
        cursor.execute(insert_query, rates_insert_values)
    cnx.commit()
    return 200

def add_currencies(
    currencies : Dict,
    table_name : str,
):
    for currency in currencies:
        insert_mysql_values(currency, table_name)
    return 200

add_currencies(currencies, 'exchange_rates')
