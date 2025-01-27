import psycopg2
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
                cont = input(f"Type \033[33m-q\033[m to quit or press \033[33mENTER\033[m to try again:")

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
            cont = input(f"Type \033[33m-q\033[m to quit or press \033[33mENTER\033[m to try again:")

            if cont == '-q':
                conn = None
                break

        except (Exception,psycopg2.DatabaseError,psycopg2.OperationalError) as Error:
            print(f"\033[31m\n[!] An error occured:\033[m \033[31m{Error}\033[m")
            cont = input(f"Type \033[33m-q\033[m to quit or press \033[33mENTER\033[m to try again:")

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
