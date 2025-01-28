def int_one_to_three():
    while True:
        try:
            choice = int(input("\n\033[1;3mChoice:\033[m "))
            if 1 < choice > 3:
                print("\033[31mInvalid choice!\033[m")
            else:
                return choice

        except ValueError:
            print("\033[31mInvalid Format!\033[m ")

def yes_or_no(message):
    while True:
        yes_no = input(f"{message} Y/N: ").strip().capitalize()
        if yes_no != "Y" or yes_no != "N":
            break
        else:
            print("\033[31mInvalid Format! Answer Y or N\033[m")

    return yes_no