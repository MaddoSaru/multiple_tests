## CREATE AND SHOW DATABASES
>cursor.execute("CREATE DATABASE {database_name}")

>cursor.execute("SHOW DATABASES")

## CREATE AND SHOW TABLES
>cursor.execute("CREATE TABLE {table_name}")

>cursor.execute("CREATE TABLE exchange_rates (currency VARCHAR(255), timestamp TIMESTAMP, rate DOUBLE)")

>cursor.execute("SHOW TABLES")

## INSERT VALUES TO A TABLE
>rates_insert_values = ('BTC',datetime.now(),20543.226)

>cursor.execute(build_insert_query('exchange_rates'), rates_insert_values)

>cnx.commit()