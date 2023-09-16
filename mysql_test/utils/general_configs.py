import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host' : '127.0.0.1',
    'port' : 3306,
    'user' : 'root',
    'password' : os.getenv("MYSQL_ROOT_PASS"),
    'database' : 'test'
}

query_types = {
    'read_query' : 'utils/queries/read_query.sql',
    'insert_query' : 'utils/queries/insert_data.sql',
    'get_min_time_query' : 'utils/queries/get_min_time.sql',
    'get_max_time_query' : 'utils/queries/get_max_time.sql',
}

currencies = {
    'BTC'
}

cryptocompare_api_key = os.getenv("CRYPTOCOMPARE_API_KEY")
