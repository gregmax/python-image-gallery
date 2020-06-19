import sys
import db_functions


# Main menu system
def menu():
    print('1) List users\n2) Add user\n3) Edit user\n4) Delete user\n5) Quit')
    option = int(input("Enter command> "))
    menu_options(option)


# Route user input to menu selection
def menu_options(option):
    if option == 1:
        db_functions.connect()
        db_functions.list_users()
        menu()

    elif option == 2:
        db_functions.connect()
        db_functions.add_user()
        menu()

    elif option == 3:
        db_functions.connect()
        db_functions.edit_user()
        menu()

    elif option == 4:
        db_functions.connect()
        db_functions.delete_user()
        menu()

    elif option == 5:
        sys.exit('Bye.')

    else:
        print(str(option) + " is not a valid option. Please try again.")
        menu()


menu()
