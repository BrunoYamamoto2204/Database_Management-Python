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
cur = connection.cursor()
connection.autocommit = True

table_management.list_tables_columns(connection)

columns_name = ''
column_values = ''

print("\n\033[1;34mINSERT DATA:\033[m")
table_name = input("Table Name: ")
table_columns = table_management.list_column_names_type(connection, table_name)
print()

if len(table_columns) == 0:
    print(f"\033[31m[!] {table_name} table do not exist\033[m")
else:
    for column in range(len(table_columns)):

        primary_keys = table_management.is_pk(connection, table_name)
        if table_columns[column][0] in primary_keys:
            continue

        column_value = input(f"\033[36m{table_columns[column][0]}:\033[m ")

        # Verifying if it is the last column
        if column == len(table_columns)-1:
            columns_name += table_columns[column][0]

            # Verify if column have string type
            if table_columns[column][1] == 'character varying':
                column_values += f"'{column_value}'"
            else:
                column_values += column_value

        # Have more columns
        else:
            columns_name += table_columns[column][0] + ","

            # Verify if column have string type
            if table_columns[column][1] == 'character varying':
                column_values += f"'{column_value}',"
            else:
                column_values += column_value + ","

    print(f"Table name: {table_name}")
    print(f"Columns Name: {columns_name}")
    print(f"Columns Values: {column_values}")

    try:
        insert_query = f"INSERT INTO {table_name}({columns_name}) VALUES ({column_values})"
        cur.execute(insert_query)
        print(f"\n\033[33mFinal query:\033[m {insert_query}")
        print("\033[32m[+] New values has been entered!\033[m")
    except (psycopg2.errors.UniqueViolation, Exception) as error:
        print("=" * 40)
        print("\n\n\033[31m[!] Something went wrong while creating the table\033[m")
        print(error)

print("=" * 40)


