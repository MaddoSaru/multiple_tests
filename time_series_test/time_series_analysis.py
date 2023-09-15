import mysql.connector
from datetime import datetime
from utils.configs import db_config
import pandas as pd

file_open = open('utils/queries/read_data.sql', 'r')
str_query = file_open.read()

def build_time_series_df(
    table_name : str,
    str_query : str
):
    read_query = str_query.format(table_name = table_name)
    cnx = mysql.connector.connect(** db_config)    
    cursor = cnx.cursor()
    cursor.execute(read_query)

    columns_names = list(cursor.column_names)


    columns_dict = dict((item_count, columns_names[item_count]) for item_count in range(len(columns_names)))
    
    time_series_df = pd.DataFrame(list(map(lambda x: x, cursor)))
    time_series_df.rename(columns = columns_dict, inplace = True)

    return time_series_df

time_series_df = build_time_series_df('exchange_rates', str_query)
