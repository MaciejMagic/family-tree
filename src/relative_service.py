import sqlite3
import sys

from app.main import FEATURES

from relative import Relative


def relative_new(database: sqlite3.Connection) -> Relative | None:
    """
    Collects info for each attribute from user input.
    Creates a new Relative object and inserts as a row into database.
    """

    try:
        print("Provide info for a new person: ('Enter' to skip)")
        new_relative = Relative()
        for feature in FEATURES:
            feature_value = input(f"{feature.replace('_', ' ').title()}: ")
            try:
                setattr(new_relative, feature, feature_value)
            except ValueError:
                print("Input value error")
                setattr(new_relative, feature, None)

        answer = input(
            "Is the provided information correct? [Y/N] ").strip().lower()
        if answer == "y":
            result = relative_new_save(new_relative, database)
            if result in [1, 2, 3]:
                print("Adding new person unsuccessful")
                return None
            print("New relative (" + new_relative.first_name +
                  " " + new_relative.last_name + ") saved")
            return new_relative
        else:
            print("Info discarded")
            return None

    except AttributeError:
        print("Attribute value error. Info discarded")
        return None


def relative_new_save(person: Relative, database: sqlite3.Connection) -> int:
    """
    Persists a Relative object as a row in database
    """

    matches = relative_load(database, first_name=person.first_name,
                            last_name=person.last_name)

    insert_query = (
        """INSERT INTO family
           (first_name, last_name, gender, family_name, date_of_birth,
           place_of_birth, date_of_death, place_of_death, phone, email,
           events, desc, spouse, children)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""")

    feedback = f"Relative info ({person.first_name} {person.last_name}) saved successfully"

    if matches:
        print("Following people already exist with provided name:")
        for match in matches:
            print("- id:", match['id'], ", ", match['first_name'], " ",
                  match['last_name'], ", born ", match['date_of_birth'])

        answer = input(
            "Add new person with the same credentials? [Y/N] ").strip().lower()
        if answer == "y":
            pass
        else:
            print("Action cancelled")
            return 1

    try:
        insert = database.execute(insert_query, person.first_name, person.last_name,
                                  person.gender, person.family_name, person.date_of_birth,
                                  person.place_of_birth, person.date_of_death,
                                  person.place_of_death, person.phone, person.email,
                                  person.events, person.desc)
    except FileNotFoundError:
        print("Error: database file not found")
        return 2
    except sqlite3.Error:
        print("Error writing to database")
        return 3
    if insert:
        print(feedback)
    return 0


def relative_load(database: sqlite3.Connection, **kwargs) -> list[Relative] | None:
    """
    Returns a list of Relative-class objects specified by first_name and last_name
    keywords, loaded from provided database
    """

    try:
        results = database.execute("""SELECT * FROM family
                                      WHERE first_name = ? AND last_name = ?
                                      ORDER BY date_of_birth ASC""",
                                   kwargs["first_name"], kwargs["last_name"])
    except sqlite3.Error:
        print("Loading error with database", file=sys.stderr)

    if results:
        return list(map(lambda match: Relative(**match), results))

    return None


def relative_select():
    return


def relative_modify(person: Relative, info: int, content: str) -> Relative:
    """
    Modifies attributes in a Relative-class object
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


def relative_update(person: Relative, database: sqlite3.Connection) -> None:
    """
    Updates existing row in database through a Relative object
    """

    for feature in FEATURES:
        value = getattr(person, feature)

        update_query = f"""UPDATE family SET {feature} = {value} WHERE id = ?"""

        try:
            update = database.execute(update_query, person.id)
        except sqlite3.Error:
            print("Loading error with database", file=sys.stderr)

        if update:
            print(f"{feature.replace('_', ' ').title()} update successful")


def relative_delete(database: sqlite3.Connection, person: Relative) -> None:
    """
    Removes an existing relative from database
    """

    delete_query = """DELETE FROM family WHERE id = ?"""

    try:
        if person.id is None:
            print("Deletion unsuccessful - No object ID")
            return
        delete = database.execute(delete_query, person.id)
    except sqlite3.Error:
        print("Deletion error with database", file=sys.stderr)

    if delete:
        print("Deletion successful")
    else:
        print("Deletion unsuccessful")

    return


def relatives_show_all(database: sqlite3.Connection) -> str | None:
    """
    Retrieve all entries from database, print all to stdout
    """

    try:
        results = database.execute("""SELECT * FROM family
                                      ORDER BY date_of_birth ASC""")
    except sqlite3.Error:
        print("Error with loading all entries from database", file=sys.stderr)

    family_all = """\n"""

    if results:
        for person in results:
            family_all += (person["first_name"] + " " + person["last_name"] + " (" +
                           person["date_of_birth"] + " - " + person["date_of_death"] + ")" + "\n")
            return family_all

    return None


def relative_list_all(database: sqlite3.Connection):
    """
    Return a list of lists, from rows in database
    """

    return
