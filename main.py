import sqlite3
import sys

from helpers import connect_to_db, show_help
from relative_service import relative_load, relative_modify, relative_new
from visualize import generate_tree_db

FEATURES = ("first_name", "last_name", "gender", "family_name",
            "date_of_birth", "place_of_birth", "date_of_death",
            "place_of_death", "phone", "email", "events", "desc")

ARGUMENTS = ("-h", "--help")

if __name__ == "__main__":

    for argument in sys.argv:
        if argument in ARGUMENTS:
            if (argument == "-h") or (argument == "--help"):
                show_help()
                break
        else:
            sys.exit("Error: wrong command line argument")

    try:
        db_connection = connect_to_db()
        while True:
            start = input("""Welcome to Family Tree

Available options:
    1. Add new relative
    2. Modify info about existing relative
    3. Generate tree
    4. List all relatives
    5. Exit
Proceed with: """)

            # 1. Add new person to database
            if start == "1":
                while True:
                    relative_new(db_connection)
                    another = input("Add another? [Y/N] ")
                    if another == "Y":
                        pass
                    else:
                        break

            # 2. Modify existing person in database
            elif start == "2":
                # Ask for search parameters
                first_name = input("Search for first name: ")
                last_name = input("Search for last name: ")

                # Ask which info to edit
                info_to_edit = int(input("""Which info to add / edit:
1. Family name
2. Date of birth
3. Place of birth
4. Date of death
5. Place of death
6. Phone number
7. Email address
8. Events
9. Description
Proceed with: """))

                # Ask with what content to edit
                new_content = input("Enter new info: ")

                db_connection = connect_to_db("tree.db")

                # 'load_relative' function returns a list of Person objects
                results = relative_load(
                    db_connection, first_name=first_name, last_name=last_name)

                # If there are multiple people with the given name - list them
                found = len(results)
                if len(results) > 1:
                    for person in results:
                        list_item = (((len(results) + 1) - found), '. ', person.first_name,
                                     ' ', person.last_name, ', born ', person.date_of_birth)
                        print(str(list_item))
                        found -= 1

                    # Ask which entry to edit
                    person_choice = input("Which person to edit? ")

                    # Person object to edit is:
                    person_to_edit = results[int(person_choice) - 1]

                # If there are none - exit
                elif results is None:
                    sys.exit("No such person in database")

                else:
                    person_to_edit = results[0]

                edited_person = relative_modify(
                    person_to_edit, info_to_edit, new_content)

                # Save to database with modified info
                try:
                    db_connection.execute("""INSERT INTO family (?)
                                            VALUES(?) WHERE first_name = ? AND last_name = ?""",
                                          info_to_edit,
                                          new_content,
                                          edited_person.first_name,
                                          edited_person.last_name)

                    print("Modified info (" + person_to_edit.first_name +
                          " " + person_to_edit.last_name + ") saved")

                except sqlite3.Error:
                    sys.exit("Error saving to database")
                except FileNotFoundError:
                    sys.exit("File not found")

            # 3. Generate family tree
            elif start == "3":
                # If no arguments provided, generate from default database
                if len(sys.argv) == 1:
                    generate_tree_db("tree.db")
                else:
                    show_help()
                    sys.exit("Too many arguments")

            # 4. Print list of all entries in database
            elif start == "4":
                # TODO - retrieve list of all records from db and print all
                all_family = []

                # return all_family

            # 5. Exit
            elif start == "5":
                sys.exit("Program exited by user")

            else:
                show_help()
                sys.exit("Invalid input")

    except (ValueError, TypeError):
        sys.exit("Input error")
    except sqlite3.Error:
        sys.exit("Error with database")
