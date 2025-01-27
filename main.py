import ValidAnswer
import database

print("*\033[3;4m This project was made for PostgreSQL databases\033[m")
print("\033[3m- Before creating a new database, you must connect in another one (Defaul: postgres)\033[m")

while True:

    # Quit the application if type "-q"
    # Get connection with database
    conn = database.connect_database()
    if conn is None:
        break


    print("\033[1;33mCreate or access a database:\033[m")
    print("[ 1 ] Access a Database")
    print("[ 2 ] Create a Database")
    ValidAnswer.create_access()
    break



