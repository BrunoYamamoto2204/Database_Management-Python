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
    create_access = ValidAnswer.create_access()

    print("-" * 40)

    if create_access == 1:
        print("Chose an action: \n")
        print("[-q] Leave application")

        choice = input("\nChoice: ")
        if choice == "-q":
            break

    if create_access == 2:
        dbName = input("New Database name: ")
        createDB = database.create_database(current_conn,dbName)

    if create_access == 3:
        current_conn = database.connect_database()
        if current_conn is None:
            continue



