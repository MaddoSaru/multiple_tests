import pandas as pd
import numpy as np
import requests
from datetime import datetime
from typing import Dict, Optional
import mysql.connector
from utils.general_configs import query_types, db_config, cryptocompare_api_key, currencies
from utils.tables_configs import tables_config

def build_query_str(
    query_type : str,
) -> str:
    open_file = open(query_types[query_type], 'r')
    return open_file.read()

def build_read_query(
    table_name : str,
    query_type : str,
    time_column_name : Optional[str]
) -> str:
    read_query = build_query_str(query_type = query_type).format(table_name = table_name) \
        if query_type == 'read_query' \
        else build_query_str(query_type = query_type).format(time_column_name = time_column_name, table_name = table_name) \
        if query_type == 'get_min_time_query' \
        else build_query_str(query_type = query_type).format(time_column_name = time_column_name, table_name = table_name) \
        if query_type == 'get_max_time_query' \
        else ''
    return read_query

def read_mysql_query(
    table_name : str,
    query_type : str,
    time_column_name : Optional[str],
) -> pd.DataFrame:
    cnx = mysql.connector.connect(** db_config)    
    cursor = cnx.cursor()
    query_str = build_read_query(table_name = table_name, query_type = query_type, time_column_name = time_column_name)
    cursor.execute(query_str)
    columns_names = list(cursor.column_names)
    columns_dict = dict((item_count, columns_names[item_count]) for item_count in range(len(columns_names)))
    query_df = pd.DataFrame(list(map(lambda x: x, cursor)))
    query_df.rename(columns = columns_dict, inplace = True)
    return query_df

def build_insert_query(
    table_name : str,
) -> str:
    field_names = str(list(tables_config[table_name])).replace("'","").replace("[","").replace("]","")
    replacement_values = '%s' + (len(tables_config[table_name]) - 1) * ',%s'
    format_str_query = build_query_str('insert_query').format(table_name = table_name, field_names = field_names, replacement_values = replacement_values)
    return format_str_query

def get_refill_cryptocompare_rates_df(
    currency : str,
    endpoint : str,
) -> pd.DataFrame:
    aux_min_time = read_mysql_query(
        table_name = 'cryptocompare_currencies_exchange_rates',
        query_type = 'get_min_time_query',
        time_column_name = 'time',
    )['min_time'][0]
    min_time = datetime.now().timestamp() if aux_min_time is None else aux_min_time
    url = f'https://min-api.cryptocompare.com/data/v2/{endpoint}?fsym={currency}&tsym=USD&toTs={min_time}&api_key={cryptocompare_api_key}&limit=2000'
    request = requests.get(url = url).json()['Data']['Data']
    rates_df = pd.DataFrame(request)
    rates_df['currency'] = currency
    return rates_df

def get_fill_cryptocompare_rates_df(
    currency : str,
    endpoint : str,
) -> pd.DataFrame:
    max_time = read_mysql_query(
        table_name = 'cryptocompare_currencies_exchange_rates',
        query_type = 'get_max_time_query',
        time_column_name = 'time',
    )['max_time'][0]
    url = f'https://min-api.cryptocompare.com/data/v2/{endpoint}?fsym={currency}&tsym=USD&api_key={cryptocompare_api_key}&limit=2000'
    request = requests.get(url = url).json()['Data']['Data']
    rates_df = pd.DataFrame(request)
    rates_df['currency'] = currency
    rates_df = rates_df[rates_df['time'] > max_time]
    return rates_df

def insert_rates_values(
    currency : str,
    table_name : str,
    endpoint : str,
    method : str,
):
    rates_df = get_refill_cryptocompare_rates_df(currency = currency, endpoint = endpoint) if method == 'refill' else get_fill_cryptocompare_rates_df(currency = currency, endpoint = endpoint)
    insert_query = build_insert_query(table_name = table_name)
    cnx = mysql.connector.connect(** db_config)
    for index in rates_df.index:
        insert_values = list(map(lambda x: rates_df[x][index], tables_config[table_name]))
        for value_index in range(len(insert_values)):
            if isinstance(insert_values[value_index], (np.int64, np.float64)):
                insert_values[value_index] = insert_values[value_index].item()
        cursor = cnx.cursor()
        cursor.execute(insert_query, insert_values)
    cnx.commit()
    return 200

def add_currencies(
    table_name : str,
    endpoint : str,
    method : str
) -> None:
    for currency in currencies:
        insert_rates_values(currency = currency, table_name = table_name, endpoint = endpoint, method = method)
    return 200
