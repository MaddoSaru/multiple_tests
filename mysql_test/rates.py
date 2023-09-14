import pandas as pd
import mysql.connector
from datetime import datetime
import requests
from typing import Dict
from dotenv import load_dotenv
import os
from utils.functions.general_functions import add_currencies

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

file_open = open('utils/queries/insert_data.sql', 'r')
str_query = file_open.read()

add_currencies(
    currencies = currencies, 
    table_name = 'exchange_rates', 
    tables_config = tables_config, 
    str_query = str_query,
    api_key = api_key,
    db_config = db_config
)
