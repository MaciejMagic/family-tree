import sqlite3

from main import FEATURES
from relative import Relative


def relative_new(database: sqlite3.Connection) -> Relative | None:
    """
    Collects basic info from user input - only for 3 required positional arguments.
    Creates a new Relative-class object and inserts this data into db.
    """

    while True:
        try:
            print("Provide info for a new person: ('Enter' to skip)")
            person_new_dict = {}
            for feature in FEATURES:
                feature_new = input(f"{feature.replace('_', ' ').title()}: ")
                person_new_dict[feature] = feature_new

            answer = input("Is the provided information correct? [Y/N] ")
            if answer == "Y":
                new_relative = Relative(**person_new_dict)
                result = relative_save(new_relative, database)
                if result in [1, 2, 3, 4]:
                    print("Adding new person unsuccessful")
                    return None
                save_feedback = ("New relative (", new_relative.first_name,
                                 " ", new_relative.last_name, ") saved")
                print(str(save_feedback))
                return new_relative
            if answer == "N":
                pass
            else:
                print("Info discarded")
                return None
        except ValueError as exc:
            raise ValueError from exc


def relative_save(person: Relative, database: sqlite3.Connection) -> int:
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

    insert_query = (
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
                result = database.execute(insert_query, person.first_name,
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
        if answer == "N":
            print("Action cancelled")
            return 3

        print("Wrong input")
        return 4

    else:
        result = database.execute(insert_query, person.first_name,
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


def relative_delete(database: sqlite3.Connection, person: Relative) -> None:
    """
    Removes an existing relative from database
    """

    delete_query = """DELETE FROM family WHERE first_name = ? AND last_name = ? AND id = ?"""

    try:
        delete = database.execute(
            delete_query, person.first_name, person.last_name, person.id)
    except sqlite3.Error as exc:
        raise sqlite3.Error from exc

    if delete:
        print("Deletion successful")
    else:
        print("Deletion unsuccessful")

    return


def relative_show_all(database: sqlite3.Connection) -> str:
    """ Print all relatives from database """

    # TODO - retrieve list of all records from db and print all

    pass
