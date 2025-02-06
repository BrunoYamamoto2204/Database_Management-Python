import psycopg2
import database
import table_management

#Ver se é PRIMARY KEY
connection = psycopg2.connect(
    database = 'teste',
    user = 'postgres',
    password = '',
    host = 'localhost',
    port = 5432
)


database.insert_data(connection)

