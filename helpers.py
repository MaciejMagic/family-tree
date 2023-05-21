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


def relative_new() -> None:
    """
    Collects basic info from user input - only for 3 required positional arguments.
    Creates a new Relative-class object and inserts this data into db.
    """

    while True:
        try:
            first_name = input("First name: ")
            last_name = input("Last name: ")
            gender = input("Gender (female / male): ")

            answer = input("Is the provided information correct? [Y/N] ")
            if answer == "Y":
                db_connection = connect_to_db("tree.db")
                new_relative = Relative(first_name, last_name, gender)
                result = relative_save(new_relative, db_connection)
                if result in [1, 2, 3, 4]:
                    print("Adding new person unsuccessful")
                    return
                save_feedback = ("New relative (", new_relative.first_name,
                                 " ", new_relative.last_name,
                                 ") saved in tree.db")
                print(str(save_feedback))
                return
            if answer == "N":
                pass
            else:
                print("Info discarded")
                return
        except ValueError as exc:
            raise ValueError from exc


def relative_save(person: Relative, database: sqlite3.Connection):
    """
    Persists a Relative object as a new entry/row in database
    """

    try:
        matches = database.execute("""SELECT * FROM family
                                    WHERE first_name = ?
                                    AND last_name = ?""",
                                   person.first_name, person.last_name)
    except sqlite3.Error as exc1:
        raise sqlite3.Error from exc1

    insert = (
        """INSERT INTO family (first_name, last_name, gender) VALUES (?, ?, ?)""")

    if len(matches) > 0:
        print("Following people already exist with provided name:")
        for match in matches:
            match_id = ('- id:', match['id'], ', ', match['first_name'], ' ',
                        match['last_name'], ', born ', match["date_of_birth"])
            print(str(match_id))

        feedback = f"Relative info ({person.first_name} {person.last_name}) saved successfully"

        answer = input("Add new person with the same credentials? [Y/N] ")
        if answer == "Y":
            try:
                result = database.execute(insert, person.first_name,
                                          person.last_name, person.gender)
            except FileNotFoundError:
                print("Error: database file not found")
                return 1
            except sqlite3.Error:
                print("Error with database")
                return 2

            if result:
                print(feedback)
            return 0
        elif answer == "N":
            print("Action cancelled")
            return 3
        else:
            print("Wrong input")
            return 4
    else:
        result = database.execute(insert, person.first_name,
                                  person.last_name, person.gender)
        if result:
            print(feedback)
        return 0


def relative_load(database: sqlite3.Connection, **kwargs) -> list[Relative] | None:
    """
    Returns a list of Relative-class objects from database,
    specified by first_name and last_name keywords
    """

    try:
        results = database.execute("""SELECT * FROM family
                                      WHERE first_name = ? AND last_name = ?""",
                                   kwargs["first_name"], kwargs["last_name"])
    except sqlite3.Error as exc:
        raise sqlite3.Error from exc

    found_relatives = []
    if results:
        for match in results:
            found_relatives.append(Relative(**match))
        return found_relatives
    else:
        return None


def relative_modify(person: Relative, info: int, content: str) -> Relative:
    """
    Modifies info of existing relative through a Relative-class object
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


def relative_delete(person: Relative) -> None:
    """
    Removes an existing relative from database
    """

    return
