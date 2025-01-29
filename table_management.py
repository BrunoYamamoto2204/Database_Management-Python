def list_tables_columns(connection):
    cur = connection.cursor()
    all_tables = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    cur.execute(all_tables)
    result_tables = cur.fetchall()

    print("\033[1m=" * 40)
    print(f"{' || Tables and columns || ':^40}")
    print("=" * 40)
    for table in result_tables:
        print(f"\033[33mTable:\033[m {table[0]}")
        all_columns = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table[0]}'"
        cur.execute(all_columns)
        result_columns = cur.fetchall()
        for column in result_columns:
            print(f"\033[36m  Column:\033[m {column[0]}")

        if table != result_tables[-1]:
            print()

    print("=" * 40)
    cur.close()

def list_column_names(connection, table):
    column_list = []

    cur = connection.cursor()
    all_columns = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'"
    cur.execute(all_columns)
    result = cur.fetchall()

    for column in result:
        column_list.append(column[0])

    cur.close()
    return column_list

def list_column_names_type(connection, table):
    column_list = []

    cur = connection.cursor()
    all_columns = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}'"
    cur.execute(all_columns)
    result = cur.fetchall()

    for column in result:
        column_list.append(column)

    cur.close()
    return column_list

def is_pk(connection, table):
    primary_keys = []

    cur = connection.cursor()
    query = f"SELECT column_name FROM information_schema.key_column_usage WHERE table_name = '{table}'"
    cur.execute(query)
    result = cur.fetchall()

    for pk in range(len(result)):
        primary_keys.append(result[pk][0])

    cur.close()
    return primary_keys