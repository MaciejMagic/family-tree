import sys
import sqlite3
from relative import Person
from visualize import generate_tree


# Initialize database
db = sqlite3.connect("tree.db")

FEATURES = ["first_name", "last_name", "gender", "family_name",
            "date_of_birth", "place_of_birth", "date_of_death",
            "place_of_death", "phone", "email", "events", "desc"]


def main():
    """ Execution of main app functions """
    try:
        start = input("""Family tree app v0.1. Choose to:
1. Add new relative
2. Modify info about existing relative
3. Generate tree
4. Exit
Proceed with: """)

        # 1. Add new person to the tree
        if start == "1":
            new_relative(database)

        # 2. Modify info
        elif start == "2":
            pass

        # 3. Generate tree using all Relative objects in existing database
        elif start == "3":
            generate_tree()

        # 4. Exit
        elif start == "4":
            sys.exit("Program exited by user")

        else:
            sys.exit("Invalid input")

    except (ValueError, TypeError):
        sys.exit("Input error")


def new_relative(database):
    """ Adding new Person object to databse """
    first_name = input("First name: ")
    last_name = input("Last name: ")
    gender = input("Gender (female / male): ")
    # TODO - adding optional info

    # Create a new person object based on the input
    relative = Person(first_name, last_name, gender)


def save_relative(person, database):
    """ Adding new Person object to databse """
    database.execute(f"""INSERT INTO family (first_name, last_name, gender)
                VALUES ({person.first_name}, {person.last_name}, {person.gender})""")

    print(f"Relative info saved ({person.first_name} {person.last_name})")


def load_relative(database, first_name=None, last_name=None):
    """ Retrieve specified relative from database """
    result = database.execute(
        f"""SELECT * FROM family
        WHERE first_name={first_name} AND last_name={last_name}""")

    loaded_person = Person(**result)

    return loaded_person


if __name__ == "__main__":
    main()
