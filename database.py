import psycopg2
import ValidAnswer
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


