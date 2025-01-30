import ValidAnswer
import database

print("*\033[3;4m This project was made for PostgreSQL databases\033[m")
print("\033[3m- Before creating a new database, you must connect in another one (Defaul: postgres)\033[m")

# Get connection with database
while True:
    # Quit the application if type "-q"
    current_conn = database.connect_database()
    if current_conn is None:
        access = False
        break
    else:
        access = True
        break

while access:
    print("-"*40)

    print("\033[1;33mCreate or access a database:\033[m")
    print(f"\033[3;34mCurrent DB:\033[m {current_conn.info.dbname}\n")
    print("[ 1 ] Enter current Database")
    print("[ 2 ] Create a new Database")
    print("[ 3 ] Access other Database")
    print("[-q ] Leave application")

    create_access = ValidAnswer.choose_or_quit(1,3)
    if create_access == "-q":
        break

    print("-" * 40)

    while True:

        if create_access == 1:
            print("\033[1;33mChose an action:\033[m \n")
            print("[1] Create Table")
            print("[2] Insert Data")
            print("[3] Edit Data")
            print("[4] Delete Data")
            print("[-q] Go Back ")

            choice = ValidAnswer.choose_or_quit(1,3)

            if choice == "-q":
                break

            if int(choice) == 1:
                table_name = input("\033[33mNew Table name: \033[m").strip()
                database.create_table(current_conn,table_name)

            if int(choice) == 2:
                database.insert_data(current_conn)

            if int(choice) == 3:
                database.update_data(current_conn)

            if int(choice) == 4:
                database.delete_data_database(current_conn)

        if create_access == 2:
            dbName = input("New Database name: ").strip()
            database.create_database(current_conn,dbName)

        if create_access == 3:
            current_conn = database.connect_database()
            if current_conn is None:
                continue



