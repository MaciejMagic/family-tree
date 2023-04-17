import sys
import csv
import sqlite3
from relative import Person
from visualize import generate_tree_csv, generate_tree_db


FEATURES = ["first_name", "last_name", "gender", "family_name",
            "date_of_birth", "place_of_birth", "date_of_death",
            "place_of_death", "phone", "email", "events", "desc"]


def main():
    """
    Execution of main app functionality:
    - connect to database
    - ask for user action
    - read / write / update database entries
    - generate SVG/PDF file
    """
    try:
        start = input("""Family tree app v0.1. Choose to:
1. Add new relative
2. Modify info about existing relative
3. Generate tree
4. List all relatives
5. Exit
Proceed with: """)

        # 1. Add new person to the tree
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
                sys.exit("Discarded")

        # 2. Modify info
        elif start == "2":
            if len(sys.argv) == 1:
                db_connection = connect_to_db("tree.db")
                # Ask for search input
                first_name = input("Search for first name: ")
                last_name = input("Search for last name: ")
                # load_relative returns a list of Person objects
                results = load_relative(db_connection, first_name=first_name, last_name=last_name)

                found = len(results)
                if found > 0:
                    for person in results:
                        print(f"{found}. {person}")
                        # Append to list ? Fix iteration
                        found -= 1
                else:
                    print("None found")

                # TO DO - Ask which entry to edit

                # TO DO - save back to db with modified info

                print(f"Modified info ({} {}) saved at tree.db")

            elif (len(sys.argv) == 2) and (sys.argv[1].endswith(".db")):
                db_connection = connect_to_db(sys.argv[1])
                # TO DO - edit info
                # print(f"Modified info ({} {}) saved at {sys.argv[1]}")

            elif (len(sys.argv) == 2) and (sys.argv[1].endswith(".csv")):
                try:
                    with open(sys.argv[1], "a") as file:
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

            return all_family

        # 5. Exit
        elif start == "5":
            sys.exit("Program exited by user")

        else:
            sys.exit("Invalid input")

    except (ValueError, TypeError):
        sys.exit("Input error")


def connect_to_db(dbfile: str = "tree.db") -> sqlite3.Connection:
    """
    Establishes a connection to specified SQLite 3 database
    """
    connection = None
    try:
        connection = sqlite3.connect(dbfile)
    except FileNotFoundError as error:
        sys.exit(error)

    return connection


def new_relative() -> Person:
    """
    Collects user input for a new Person object
    """
    first_name = input("First name: ")
    last_name = input("Last name: ")
    gender = input("Gender (female / male): ")
    # Create and return a new Person object based on user input
    return Person(first_name, last_name, gender)


def save_relative(person: Person, database: sqlite3.Connection) -> None:
    """
    Persists a Person object as a row in database
    """
    # TO DO - need to check if specified person already exists in db
    try:
        result = database.execute(f"""INSERT INTO family (first_name, last_name, gender)
                    VALUES ({person.first_name}, {person.last_name}, {person.gender})""")
    except FileNotFoundError:
        raise FileNotFoundError

    if result:
        print(f"Relative info saved ({person.first_name} {person.last_name})")


def load_relative(database: sqlite3.Connection, **kwargs) -> list[Person]:
    """
    Returns relative/s specified by name from database as a list of Person objects
    """
    try:
        results = database.execute(
            f"""SELECT * FROM family
            WHERE first_name={kwargs["first_name"]} AND last_name={kwargs["last_name"]}""")
    except FileNotFoundError:
        raise FileNotFoundError

    found_relatives = []
    if results:
        for row in results:
            found_relatives.append(Person(**row))
        return found_relatives
    else:
        print("None found")
        return None


if __name__ == "__main__":
    main()
