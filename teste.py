import psycopg2
import database
import table_management

#Ver se é PRIMARY KEY
connection = psycopg2.connect(
    database = 'teste',
    user = 'postgres',
    password = '*%(22bru04no06)?',
    host = 'localhost',
    port = 5432
)


database.delete_data_database(connection)

