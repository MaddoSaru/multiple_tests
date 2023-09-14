import pandas as pd
import requests
from datetime import datetime
from typing import Dict
import mysql.connector

def get_rates_df(
    currency : str,
    api_key : str
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
    tables_config : Dict,
    str_query : str
):
    field_names = str(tables_config[table_name]['field_names']).replace("'","")
    replacement_values = '(%s'+str( (len(tables_config[table_name]['field_names']) - 1) * ',%s')+')'
    format_str_query = str_query.format(table_name = table_name, field_names = field_names, replacement_values = replacement_values)
    return format_str_query

def insert_mysql_values(
    currency : str,
    table_name : str,
    tables_config : Dict,
    str_query : str,
    api_key : str,
    db_config : Dict,
):
    rates_df = get_rates_df(currency, api_key)
    insert_query = build_insert_query(table_name, tables_config, str_query)
    cnx = mysql.connector.connect(** db_config)
    for index in rates_df.index:
        rates_insert_values = (rates_df['currency'][index], rates_df['timestamp'][index], rates_df['rate'][index])
        cursor = cnx.cursor()
        cursor.execute(insert_query, rates_insert_values)
    cnx.commit()
    return 200

def add_currencies(
    currencies : Dict,
    table_name : str,
    tables_config : Dict,
    str_query : str,
    api_key : str,
    db_config : Dict
):
    for currency in currencies:
        insert_mysql_values(currency, table_name, tables_config, str_query, api_key, db_config)
    return 200