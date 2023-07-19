import sys

from service.helpers import arguments, connect_to_db, start
from service.relative_service import (relative_create, relative_load,
                                      relative_modify, relatives_show)
from service.visualize import generate_tree

if __name__ == "__main__":

    args = arguments()

    print(f"🌳 Input file is: {args.file_input}")
    print(f"🌳 Output file is: {args.file_output}")

    db_connection = connect_to_db(args.file_input)
    db_cursor = db_connection.cursor()

    while True:
        start_option = start()

        # 1. Add new person to database
        if start_option == 1:
            while True:
                relative_create(db_cursor)
                another = input("Add another? [Y/N] ") \
                    .strip() \
                    .lower()
                if another == "y":
                    pass
                else:
                    break

        # 2. Modify existing person in database
        elif start_option == 2:
            first_name = input("Search for a person with first name: ") \
                .strip() \
                .capitalize()
            last_name = input("Search for a person with last name: ") \
                .strip() \
                .capitalize()

            # Search for list of matches
            relatives_loaded = relative_load(
                db_cursor, first_name=first_name, last_name=last_name)

            print(relative_modify(db_cursor, relatives_loaded))

        # 3. Generate tree
        elif start_option == 3:
            generate_tree(db_cursor)

        # 4. Print a simplified list of all relatives
        elif start_option == 4:
            print(relatives_show(db_cursor))

        # 5. Print a detailed list of all relatives
        elif start_option == 5:
            print(relatives_show(db_cursor, show_all=True))

        # 6. Exit
        elif start_option == 6:
            db_connection.close()
            sys.exit()

        else:
            db_connection.close()
            sys.exit("Wrong input")
