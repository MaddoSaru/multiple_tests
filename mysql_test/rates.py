import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

db_config = {
    'host' : '127.0.0.1',
    'port' : 3306,
    'user' : 'root',
    'password' : os.getenv("MYSQL_ROOT_PASS"),
    'database' : 'test'
}

cnx = mysql.connector.connect(** db_config)
cursor = cnx.cursor()

fd = open('utils/insert_data.sql', 'r')
sqlFile = fd.read()
print(sqlFile)

#cursor.execute("CREATE DATABASE {database_name}")
#cursor.execute("SHOW DATABASES")
#cursor.execute("CREATE TABLE {table_name}")
#cursor.execute("CREATE TABLE exchange_rates (currency VARCHAR(255), timestamp TIMESTAMP, rate DOUBLE)")
#cursor.execute("SHOW TABLES")

#for table in cursor:
#    print(table)
