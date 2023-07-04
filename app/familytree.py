import sys

from service.helpers import arguments, connect_to_db, start
from service.relative_service import (relative_modify, relative_new,
                                      relative_show_more,
                                      relatives_show_less)
from service.visualize import generate_tree

if __name__ == "__main__":

    args = arguments()

    print(f"🌳 Input file is: {args.file_input}")
    print(f"🌳 Output file is: {args.file_output}")

    db_connection = connect_to_db()
    db_cursor = db_connection.cursor()

    while True:
        start_option = start()

        # 1. Add new person to database
        if start_option == 1:
            while True:
                relative_new(db_cursor)
                another = input("Add another? [Y/N] ") \
                    .strip() \
                    .lower()
                if another == "y":
                    pass
                else:
                    break

        # 2. Modify existing person in database
        elif start_option == 2:
            first_name = input("Search for first name: ").strip()
            last_name = input("Search for last name: ").strip()
            relative_modify(db_cursor, first_name, last_name)

        # 3. Generate tree
        elif start_option == 3:
            generate_tree(db_cursor)

        # 4. Print a simplified list of all relatives
        elif start_option == 4:
            print(relatives_show_less(db_cursor))

        # 5. Print a detailed list of all relatives
        elif start_option == 5:
            print(relative_show_more(db_cursor))

        # 6. Exit
        elif start_option == 6:
            db_connection.close()
            sys.exit()

        else:
            db_connection.close()
            sys.exit("Wrong input")
