import sqlite3
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Snowflake credentials
account = os.getenv('SNOWFLAKE_ACCOUNT')
user = os.getenv('SNOWFLAKE_USER')
password = os.getenv('SNOWFLAKE_PASSWORD')
warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
database = os.getenv('SNOWFLAKE_DATABASE')
schema = os.getenv('SNOWFLAKE_SCHEMA')
role = os.getenv('SNOWFLAKE_ROLE')

missing = [name for name, value in [
    ('SNOWFLAKE_ACCOUNT', account),
    ('SNOWFLAKE_USER', user),
    ('SNOWFLAKE_PASSWORD', password),
    ('SNOWFLAKE_WAREHOUSE', warehouse),
    ('SNOWFLAKE_DATABASE', database),
    ('SNOWFLAKE_SCHEMA', schema),
] if not value]
if missing:
    raise ValueError(f"Missing Snowflake env vars: {', '.join(missing)}")

print(f"Using Snowflake: account={account}, user={user}, warehouse={warehouse}, database={database}, schema={schema}")

# Connect to SQLite
sqlite_conn = sqlite3.connect('healthcare.db')

# Read data
patients_df = pd.read_sql_query("SELECT * FROM patients", sqlite_conn)
visits_df = pd.read_sql_query("SELECT * FROM visits", sqlite_conn)

sqlite_conn.close()

# Connect to Snowflake
conn_args = {
    'account': account,
    'user': user,
    'password': password,
    'warehouse': warehouse,
    'database': database,
    'schema': schema,
    'application': 'patient_data_pipeline',
}
if role:
    conn_args['role'] = role

try:
    conn = snowflake.connector.connect(**conn_args)
except Exception as exc:
    raise RuntimeError(
        'Snowflake connection failed. Confirm SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, and SNOWFLAKE_SCHEMA are correct.'
    ) from exc

# Create tables if not exist (optional, or assume they exist)
# For simplicity, use write_pandas which can create or replace

# Upload patients
write_pandas(conn, patients_df, 'PATIENTS', auto_create_table=True)

# Upload visits
write_pandas(conn, visits_df, 'VISITS', auto_create_table=True)

# Close connection
conn.close()

print("Data uploaded to Snowflake successfully")