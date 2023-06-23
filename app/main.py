import sys

from service.helpers import arguments, connect_to_db, start
from service.relative_service import (relative_modify, relative_new,
                                      relative_show_more,
                                      relatives_show_less)
from service.visualize import generate_tree

if __name__ == "__main__":

    args = arguments()

    db_connection = connect_to_db()

    while True:
        start_option = start()

        # 1. Add new person to database
        if start_option == 1:
            while True:
                relative_new(db_connection)
                another = input("Add another? [Y/N] ").strip().lower()
                if another == "y":
                    pass
                else:
                    break

        # 2. Modify existing person in database
        elif start_option == 2:
            first_name = input("Search for first name: ").strip()
            last_name = input("Search for last name: ").strip()
            relative_modify(db_connection, first_name, last_name)

        # 3. Generate tree
        elif start_option == 3:
            generate_tree(db_connection)

        # 4. Print a simplified list of all relatives
        elif start_option == 4:
            print(relatives_show_less(db_connection))

        # 5. Print a detailed list of all relatives
        elif start_option == 5:
            print(relative_show_more(db_connection))

        # 6. Exit
        elif start_option == 6:
            sys.exit()

        else:
            print("Wrong input")
