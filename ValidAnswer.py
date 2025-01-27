def create_access():
    while True:
        try:
            choice = int(input("\n\033[33mChoice:\033[m "))
            if 1 < choice > 3:
                print("\033[31mInvalid choice!\033[m")
            else:
                return choice

        except ValueError:
            print("\033[31mInvalid Format!\033[m ")

