import sqlite3
import sys

from relative import Relative


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


def relative_new() -> Relative:
    """
    Creates a Relative object from user input
    """

    first_name = input("First name: ")
    last_name = input("Last name: ")
    gender = input("Gender (female / male): ")

    # Create and return a new Relative object based on user input
    return Relative(first_name, last_name, gender)


def relative_save(person: Relative, database: sqlite3.Connection) -> None:
    """
    Persists a Relative object as a new row in database
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
    elif answer == "N":
        print("Action cancelled")
    else:
        print("Wrong input")


def relative_load(database: sqlite3.Connection, **kwargs) -> list[Relative] | None:
    """
    Returns relative/s specified by name from database as a list of Person objects
    """

    try:
        results = database.execute("""SELECT * FROM family
                                      WHERE first_name = ? AND last_name = ?""",
                                   kwargs["first_name"], kwargs["last_name"])
    except sqlite3.Error as exc:
        raise sqlite3.Error from exc

    # Print list of entries matched by SQL query
    found_relatives = []
    if results:
        for row in results:
            found_relatives.append(Relative(**row))
        return found_relatives
    else:
        return None


def relative_modify(person: Relative, info: int, content: str) -> Relative:
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


def relative_summary(person: Relative) -> dict | None:
    """ Print all availible info about this person """

    info = {
        "First name": person.first_name,
        "Last name": person.last_name,
        "Gender": person.gender,
        "Family name": person.family_name,
        "Date of birth": person.date_of_birth,
        "Place of birth": person.place_of_birth,
        "Date of death": person.date_of_death,
        "Place of death": person.place_of_death,
        "Phone number": person.phone,
        "Email address": person.email,
        "Events": person.events,
        "Description": person.desc
    }

    return info
