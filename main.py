import sys
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
    - ask user for desired action
    - read, write, update database
    - generation of svg file
    """
    # Initialize database
    # TO DO - load database from user input - arg vector
    # Default value - tree.db
    # connect_to_db(sys.argv[1])
    db_connection = connect_to_db("tree.db")

    try:
        start = input("""Family tree app v0.1. Choose to:
1. Add new relative
2. Modify info about existing relative
3. Generate tree
4. Exit
Proceed with: """)

        # 1. Add new person to the tree
        if start == "1":
            add_person = new_relative()
            answer = input("Is the provided information correct? (Y/N) ")
            if answer == "Y":
                save_relative(add_person, db_connection)
            else:
                sys.exit("Discarded")

        # 2. Modify info
        elif start == "2":
            # TO DO add new function for inserting partial info
            pass

        # 3. Generate tree using all Person objects in existing database
        elif start == "3":
            generate_tree_db()

        # 4. Exit
        elif start == "4":
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
    # TO DO - adding optional info

    # Create and return a new Person object based on the input
    relative = Person(first_name, last_name, gender)

    return relative


def save_relative(person: Person, database: sqlite3.Connection) -> None:
    """
    Persists a Person object as a row in database
    """
    # TO DO - need to check if specified person already exists in db

    database.execute(f"""INSERT INTO family (first_name, last_name, gender)
                VALUES ({person.first_name}, {person.last_name}, {person.gender})""")

    print(f"Relative info saved ({person.first_name} {person.last_name})")


def load_relative(database: sqlite3.Connection, **kwargs) -> list[Person]:
    """
    Retrieves relative/s specified by name from database as a list of Person objects
    """
    results = database.execute(
        f"""SELECT * FROM family
        WHERE first_name={kwargs["first_name"]} AND last_name={kwargs["last_name"]}""")

    found_relatives = []
    for row in results:
        found_relatives.append(Person(**row))

    return found_relatives


if __name__ == "__main__":
    main()
