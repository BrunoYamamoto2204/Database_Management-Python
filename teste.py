import psycopg2

conn = psycopg2.connect(
    database = 'sakila',
    user = 'postgres',
    password = '*%(22bru04no06)?',
    host = 'localhost',
    port = 5432
)

conn.autocommit = True
cur = conn.cursor()

query = "CREATE DATABASE teste"
cur.execute(query)
