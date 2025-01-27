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
                print("\033[31m[!] Invalid Port: Must be an integer number!\033[m")
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
            print(f"\033[31m[!] Connect failed! Invalid parameters:")

        except (Exception,psycopg2.DatabaseError,TypeError,psycopg2.OperationalError) as Error:
            print(f"\033[4;31m\nAn error occured:\033[m \033[31m{Error}\033[m")
            cont = input(f"Type \033[33m-q\033[m to quit or press \033[33mENTER\033[m to try again:")

            if cont == '-q':
                conn = None
                break

    return conn

# def create_database():
