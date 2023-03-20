import pandas as pd
import psycopg2
import csv
import os
from dotenv import load_dotenv

# def configuration files
load_dotenv()
host = os.getenv('pg_host')
port = os.getenv('pg_port')
dbname = os.getenv('pg_dbname')
user = os.getenv('pg_user')
password = os.getenv('pg_pass')

# connect to postgresql
try:
    conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
            )
    
    print('Database connection success')
except:
    print('Database connection error')

# Open a cursor to perform database operations
cur = conn.cursor()

# Define the SQL query to create the table if it does not exist
create_table_sql = """
    CREATE TABLE IF NOT EXISTS precipitation_lasvegas (
        date DATE PRIMARY KEY,
        precipitation DECIMAL(5, 2),
        precipitation_normal DECIMAL(5, 2)
    )
"""
# Execute the query to create the table
cur.execute(create_table_sql)

# Specify the path and filename of the CSV file
csv_path = '../output-data/dataclean-precipitation-lasvegas.csv'

# Open the CSV file and insert its contents into the database
with open(csv_path, 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')

    # Skip the header row
    next(csv_reader)

    # Loop through each row in the CSV file and insert it into the database
    for row in csv_reader:
        date = row[0]
        precipitation = row[1]
        precipitation_normal = row[2]

        # Define the SQL query to insert a row into the database
        sql = """
            INSERT INTO precipitation_lasvegas (date, precipitation, precipitation_normal)
            VALUES (%s, %s, %s)
        """

        # Execute the query
        cur.execute(sql, (date, precipitation, precipitation_normal))

# Commit the changes to the database
conn.commit()

# Close the database connection
cur.close()
conn.close()

print('Database insertion success')