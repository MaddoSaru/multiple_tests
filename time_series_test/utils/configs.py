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