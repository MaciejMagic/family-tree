import sys
import sqlite3


# Initialize database
db = sqlite3.connect("tree.db")

# dataclass ?
class Relative():
    def __init__(self, first_name, last_name, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        # self.family_name = family_name
        # self.date_of_birth = date_of_birth
        # self.place_of_birth = place_of_birth
        # self.date_of_death = date_of_death
        # self.place_of_death = place_of_death
        # self.phone = phone
        # self.email = email
        # self.events = events
        # self.desc = desc

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if (first_name is None) or (14 < len(first_name) < 2):
            raise ValueError
        self._first_name = first_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        if (last_name is None) or (35 < len(last_name) < 2):
            raise ValueError
        self._last_name = last_name

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        self._gender = gender

    def __str__():
        return f"{self._first_name} {self._last_name}"


def main():
    # Options what to do with the app
    try:
        start = input("""Family tree app v0.1.
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

    except ValueError, TypeError:
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


def generate_tree():
    pass


if __name__ == "__main__":
    main()
