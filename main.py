import sys
import sqlite3
from relative import Relative
from visualize import generate_tree


# Initialize database
db = sqlite3.connect("tree.db")


def main():
    # Options what to do with the app
    try:
        start = input("""Family tree app v0.1. Choose to:
                         1. Add new relative
                         2. Modify info of existing relative
                         3. Generate tree
                         4. Exit
                         Proceed with: """)

        # 1. Add new person to the tree
        if start == "1":
            new_relative()

        # 2. Modify info
        elif start == "2":
            pass

        # 3. Generate tree using existing db
        elif start == "3":
            generate_tree()

        # 4. Exit
        elif start == "4":
            sys.exit("Program exited by user")

        else:
            sys.exit("Invalid input")

    except (ValueError, TypeError):
        sys.exit("Invalid input")


def new_relative():
    first_name = input("First name: ")
    last_name = input("Last name: ")
    gender = input("Gender (female / male): ")
    # Optional (adding info as a function?)
    # date_of_birth = input("Date of birth (YYYY-MM-DD): ")

    # Create a new person object based on the input
    new_relative = Relative(first_name, last_name, gender)

    # Add new person to db
    db.execute("""INSERT INTO family
                  (first_name, last_name, gender) VALUES (?, ?, ?)""",
                  new_relative.first_name, new_relative.last_name, new_relative.gender)

    return f"{new_relative.first_name} {new_relative.last_name} added"


if __name__ == "__main__":
    main()
