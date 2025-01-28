import psycopg2
import database

conn = psycopg2.connect(
    database = 'teste',
    user = 'postgres',
    password = '*%(22bru04no06)?',
    host = 'localhost',
    port = 5432
)

database.create_table(conn,"tabela_teste2")
