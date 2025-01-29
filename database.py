import psycopg2
import ValidAnswer
import table_management
def connect_database():
    while True:
        try:
            print("\n\033[1;33mAccessing Database\033[m")

            Database = input("Database: ")
            User = input("User: ")
            Password = input("Password: ")
            Host = input("Host (Default: localhost): ") or "localhost"
            Port = input("Port (Default: 5432): ") or 5432

            try:
                Port = int(Port)
            except ValueError:
                print("\n\033[31m[!] Invalid Port: Must be an integer number!\033[m")
                cont = input(f"Type \033[33m-q\033[m to quit or press \033[33mENTER\033[m to try again:").strip()

                if cont == '-q':
                    conn = None
                    break

                continue

            conn = psycopg2.connect(
                database = Database,
                user = User,
                password = Password,
                host = Host,
                port = Port
            )

            # If no errors, return the connection
            print("\033[32m[+] Database connected successfully\033[m\n")
            break

        except psycopg2.OperationalError as error:
            error_message = str(error)
            print(f"\033[31m\n[!] Connect failed! Invalid parameters\033[m")
            cont = input(f"Type \033[33m-q\033[m to quit or press \033[33mENTER\033[m to try again:").strip()

            if cont == '-q':
                conn = None
                break

        except (Exception,psycopg2.DatabaseError,psycopg2.OperationalError) as Error:
            print(f"\033[31m\n[!] An error occured:\033[m \033[31m{Error}\033[m")
            cont = input(f"Type \033[33m-q\033[m to quit or press \033[33mENTER\033[m to try again:").strip()

            if cont == '-q':
                conn = None
                break

    return conn

def create_database(connection, dbname):
    try:
        connection.autocommit = True
        cur = connection.cursor()
        create_query = f"CREATE DATABASE {dbname}"
        cur.execute(create_query)

        # Save the changes
        connection.commit()
        print("\033[32m[+] New database has been created!\033[m")
        return True

    except psycopg2.errors.DuplicateDatabase:
        print(f"\033[31m[-] {dbname} database already exists!\033[m")
        return False

    except (Exception, psycopg2.DatabaseError):
        print("\033[31m[-] FAILED TO CONNECT!\033[m")
        connection.rollback()

def create_table(connection, table_name):
    cur = connection.cursor()
    connection.autocommit = True

    try:
        create_table = f"CREATE TABLE {table_name}("
        print("\033[1;4*Create other columns before FK\033[m\n")
        while True:
            print("-"*40)
            print("\033[33mType of column: \033[m")
            print("[1] Primary Key")
            print("[2] Foreign Key")
            print("[3] Normal data")
            column_choice = ValidAnswer.int_one_to_three()

            if column_choice == 1:
                print("\n\033[1;34mPRIMARY KEY:\033[m")
                print("\033[4m*Serial Primary Key\033[m\n")
                pk = input("Column Name: ").strip()
                pk_query = f"{pk} SERIAL PRIMARY KEY"

                create_table += pk_query

            if column_choice == 2:
                try:
                    print("\n\033[1;34mFOREIGN KEY:\033[m")
                    print("\033[4m* Reference Column must be UNIQUE or PK\033[m")
                    print("\033[4m* FOREIGN KEY(Foreign_Column) REFERENCES Reference_Table(Reference_Column)\033[m\n")

                    foreign_column = input("\033[33mForeign Column:\033[m ").strip()
                    reference_table = input("\033[33mReference Table:\033[m ").strip()
                    reference_column = input("\033[33mReference Column:\033[m ").strip()
                except:
                    print("\033[31m[!] Table or columns names do not match!\033[m")
                    continue

                else:
                    fk_query = f"FOREIGN KEY({foreign_column}) REFERENCES {reference_table}({reference_column})"
                    create_table += fk_query

            if column_choice == 3:
                print("\n\033[1;34mNORMAL DATA:\033[m")
                column_name = input("\033[33mColumn Name: \033[m").strip()
                column_type = input("\033[33mColumn Type: \033[m").strip().upper()
                not_null = ValidAnswer.yes_or_no("\033[33mNot NULL?\033[m")
                unique = ValidAnswer.yes_or_no("\033[33mUNIQUE?\033[m")

                column_query = f"{column_name} {column_type}"

                if not_null == "Y":
                    column_query += " NOT NULL"
                if unique == "Y":
                    column_query += " UNIQUE"

                create_table += column_query

            # Add more columns or create the table
            print("-" * 40)
            more_columns = ValidAnswer.yes_or_no("More columns?")

            if more_columns == "Y":
                create_table += ","

            else:
                create_table += ");"
                cur.execute(create_table)
                print("\033[32m[+] New table has been created!\033[m")
                break

        # Save changes
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("\033[31m[-] FAILED TO CREATE!\033[m")
        print(error)
        connection.rollback()

    finally:
        print("\033[33mFinal query: \033[m" + create_table)
        print("-" * 40)


def insert_data(connection):
    cur = connection.cursor()
    connection.autocommit = True

    # List all tables and their columns
    table_management.list_tables_columns(connection)

    columns_name = ''
    column_values = ''

    print("\033[1;4m*Primary Keys are SERIAL and don't need a value\033[m\n")
    print("\n\033[1;34mINSERT DATA:\033[m")
    table_name = input("Table Name: ")
    table_columns = table_management.list_column_names_type(connection, table_name)
    print()

    # If return with no columns, it doesn't exist
    if len(table_columns) == 0:
        print(f"\033[31m[!] {table_name} table do not exist\033[m")

    else:
        for column in range(len(table_columns)):

            # Check PKs of the table
            primary_keys = table_management.is_pk(connection, table_name)
            if table_columns[column][0] in primary_keys:
                continue

            # Insert value
            column_value = input(f"\033[36m{table_columns[column][0]}:\033[m ")

            # Verifying if it is the last column
            if column == len(table_columns) - 1:
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

        # Check if it has been added to the table
        try:
            insert_query = f"INSERTO INTO {table_name}({columns_name}) VALUES ({column_values})"
            cur.execute(insert_query)
            print(f"\nFinal query: {insert_query}")
            print("\033[32m[+] New values has been entered!\033[m")
        except (psycopg2.errors.UniqueViolation, Exception) as error:
            print("="*40)
            print("\n\n\033[31m[!] Something went wrong while creating the table\033[m")
            print(error)

    print("=" * 40)
    cur.close()