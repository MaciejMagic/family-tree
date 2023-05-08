import csv
import sqlite3
import sys

from helpers import (connect_to_db, load_relative, modify_relative,
                     new_relative, save_relative)
from visualize import generate_tree_csv, generate_tree_db

FEATURES = ["first_name", "last_name", "gender", "family_name",
            "date_of_birth", "place_of_birth", "date_of_death",
            "place_of_death", "phone", "email", "events", "desc"]


if __name__ == "__main__":
    try:
        start = input("""Welcome to Family Tree.
1. Add new relative
2. Modify info about existing relative
3. Generate tree
4. List all relatives
5. Exit
Proceed with: """)

        # 1. Add new person to database
        if start == "1":
            add_new_relative = new_relative()
            answer = input("Is the provided information correct? (Y/N) ")
            if answer == "Y":
                if len(sys.argv) == 1:
                    # If no arguments provided save to default database
                    db_connection = connect_to_db("tree.db")
                    save_relative(add_new_relative, db_connection)
                    print("New relative saved in tree.db")

                elif (len(sys.argv) == 2) and (sys.argv[1].endswith(".db")):
                    # If custom .db file provided, save there
                    db_connection = connect_to_db(sys.argv[1])
                    save_relative(add_new_relative, db_connection)
                    print(
                        f"New relative ({add_new_relative.first_name} {add_new_relative.last_name}) saved in {sys.argv[1]}")

                elif (len(sys.argv) == 2) and (sys.argv[1].endswith(".csv")):
                    try:
                        with open(sys.argv[1], "a", encoding="UTF-8") as file:
                            writer = csv.DictWriter(file, fieldnames=FEATURES)
                            writer.writerow(add_new_relative.__dict__)
                    except FileNotFoundError:
                        sys.exit("File not found")
                else:
                    sys.exit()
            else:
                sys.exit("Person info not correct. Discarded. Exited")

        # 2. Modify existing person in database
        elif start == "2":
            # Ask for search input
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

            if len(sys.argv) == 1:
                db_connection = connect_to_db("tree.db")

                # 'load_relative' function returns a list of Person objects
                results = load_relative(
                    db_connection, first_name=first_name, last_name=last_name)

                # If there are multiple people with the given name - list them
                found = len(results)
                if len(results) > 1:
                    for person in results:
                        print(
                            f"""{(len(results) + 1) - found}. {person.first_name} {person.last_name}, {person.date_of_birth}""")
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

                edited_person = modify_relative(
                    person_to_edit, info_to_edit, new_content)

                # TO DO - offload sql to a function ?

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

            elif (len(sys.argv) == 2) and (sys.argv[1].endswith(".db")):
                db_connection = connect_to_db(sys.argv[1])
                # TO DO - edit info
                # print(f"Modified info ({} {}) saved at {sys.argv[1]}")

            elif (len(sys.argv) == 2) and (sys.argv[1].endswith(".csv")):
                try:
                    # Append info to csv file
                    with open(sys.argv[1], "a", encoding="UTF-8") as file:
                        writer = csv.DictWriter(file, fieldnames=FEATURES)

                        # TO DO

                        writer.writerow()

                        # print(f"Modified info ({} {}) saved at {sys.argv[1]}")

                except FileNotFoundError:
                    sys.exit("File not found")

        # 3. Generate family tree
        elif start == "3":
            # If no arguments provided, generate from default database
            if len(sys.argv) == 1:
                generate_tree_db()
            elif len(sys.argv) == 2:
                # Load the provided .csv file
                if sys.argv[1].endswith(".csv"):
                    generate_tree_csv(sys.argv[1])
                # Load the provided .db file
                elif sys.argv[1].endswith(".db"):
                    generate_tree_db(sys.argv[1])
            elif len(sys.argv) > 2:
                sys.exit("Too many arguments")
            else:
                sys.exit("Usage: python main.py ['file']")

        # 4. Print list of all entries in database
        elif start == "4":
            # TO DO - retrieve list of all records from db and print all
            all_family = []

            # return all_family

        # 5. Exit
        elif start == "5":
            sys.exit("Program exited by user")

        else:
            sys.exit("Invalid input")

    except (ValueError, TypeError):
        sys.exit("Input error")
