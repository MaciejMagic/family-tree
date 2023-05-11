import sqlite3
import sys

from relative import Person


def show_help() -> None:
    """
    Prints help instructions for user
    """

    print("""
USAGE
    $ python main.py [OPTIONS] [PATH]

ARGUMENTS:
    PATH            provide a custom database file (*.db) in current dir

OPTIONS:
    -h, --help      show help

""")


def connect_to_db(dbfile: str = "tree.db") -> sqlite3.Connection | None:
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
    Creates a Person object from user input
    """

    first_name = input("First name: ")
    last_name = input("Last name: ")
    gender = input("Gender (female / male): ")

    # Create and return a new Person object based on user input
    return Person(first_name, last_name, gender)


def save_relative(person: Person, database: sqlite3.Connection) -> None:
    """
    Persists a Person object as a new row in database
    """

    try:
        exists = database.execute("""SELECT * FROM family
                                    WHERE first_name = ?
                                    AND last_name = ?""",
                                  person.first_name, person.last_name)
    except sqlite3.Error as exc1:
        raise sqlite3.Error from exc1

    if len(exists) > 0:
        print("Following people already exist with provided name:")
        for match in exists:
            print(
                f"- {match['first_name']} {match['last_name']}, born {match['date_of_birth']}")

    answer = input("Are you sure? [Y/N] ")
    if answer == "Y":
        try:
            result = database.execute("""INSERT INTO family
                                         (first_name, last_name, gender)
                                         VALUES (?, ?, ?)""",
                                      person.first_name,
                                      person.last_name,
                                      person.gender)
        except FileNotFoundError as exc2:
            raise FileNotFoundError from exc2

        if result:
            print(
                f"Relative info ({person.first_name} {person.last_name}) saved successfully")
    else:
        print("Wrong input / Action cancelled")


def load_relative(database: sqlite3.Connection, **kwargs) -> list[Person] | None:
    """
    Returns relative/s specified by name from database as a list of Person objects
    """

    try:
        results = database.execute("""SELECT * FROM family
                                      WHERE first_name = ? AND last_name = ?""",
                                   kwargs["first_name"], kwargs["last_name"])
    except sqlite3.Error as exc:
        raise sqlite3.Error from exc

    found_relatives = []
    if results:
        for row in results:
            found_relatives.append(Person(**row))
        return found_relatives
    else:
        return None


def modify_relative(person: Person, info: int, content: str) -> Person:
    """
    Modifies info of existing relative through a Person object
    """

    match info:
        case 1:
            person.family_name(content)
        case 2:
            person.date_of_birth(content)
        case 3:
            person.place_of_birth(content)
        case 4:
            person.date_of_death(content)
        case 5:
            person.place_of_death(content)
        case 6:
            person.phone(content)
        case 7:
            person.email(content)
        case 8:
            person.events(content)
        case 9:
            person.desc(content)
        case _:
            print("Wrong input")

    return person
