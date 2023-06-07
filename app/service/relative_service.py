import sqlite3
import sys

from model.relative import FEATURES, Relative
from tabulate import tabulate


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
        print("Error: loading from database", file=sys.stderr)

    if results:
        return list(map(lambda match: Relative(**match), results))

    return None


def relative_select_all(database: sqlite3.Connection) -> sqlite3.Cursor | None:
    """ Selects all rows in database. Returns a cursor object """

    try:
        results = database.execute("""SELECT * FROM family
                                      ORDER BY date_of_birth ASC""")
    except sqlite3.Error:
        print("Error: loading all entries from database", file=sys.stderr)

    if not results:
        return None
    return results


def relative_mod_attr(person: Relative, info: int, content: str) -> Relative:
    """
    Modifies an attribute in a Relative-class object
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
            print("Error: wrong input for attribute modification")

    return person


def relative_modify(database: sqlite3.Connection, first_name, last_name) -> None:
    """
    Modifies an existing person from database
    """

    # Search for list of matches
    relatives_loaded = relative_load(
        database, first_name=first_name, last_name=last_name)

    # If there are multiple people with the given name - list them
    found = len(relatives_loaded)
    if len(relatives_loaded) > 1:
        for person in relatives_loaded:
            list_item = (((len(relatives_loaded) + 1) - found), '. ', person.first_name,
                         ' ', person.last_name, ', born ', person.date_of_birth)
            print(str(list_item))
            found -= 1

        # Ask which entry to edit
        person_choice = input("Which person to edit (type number)? ").strip()

        # Person object to edit is:
        person_to_edit = relatives_loaded[int(person_choice) - 1]

    # If there are none - exit
    elif relatives_loaded is None:
        print("Error: no such person in database")
        return
    else:
        person_to_edit = relatives_loaded[0]

    # Ask which info to edit
    info_to_edit = int(input("""Which info to add / edit:
1. Family name
2. Date of birth
3. Place of birth
4. Date of death
5. Place of death
6. Phone number
7. Email address
8. Events
9. Description
Proceed with: """).strip())

    # Ask with what new content to edit
    new_content = input("Enter new info: ").strip()

    person_edited = relative_mod_attr(
        person_to_edit, info_to_edit, new_content)

    # Save to database with modified info
    relative_update(database, person_edited)

    print("Modified info (" + person_to_edit.first_name +
          " " + person_to_edit.last_name + ") saved")


def relative_update(database: sqlite3.Connection, person: Relative) -> None:
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
        except FileNotFoundError:
            print("Error: database file not found", file=sys.stderr)

    if update:
        print(f"{feature.replace('_', ' ').title()} update successful")
    else:
        print("Update unsuccessful")


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


def relatives_show_less(database: sqlite3.Connection) -> str | None:
    """
    Retrieve all entries from database, print basic info to stdout
    """

    results = relative_select_all(database)

    if results:
        return str([(person["first_name"] + " " + person["last_name"] + " ("
                     + person["date_of_birth"] +
                     " - " + person["date_of_death"]
                     + ")" + "\n") for person in results])
    return None


def relative_show_more(database: sqlite3.Connection) -> str:
    """
    Retrieve all entries from database.
    Return a multiline string formatted as a table.
    """
    # TODO - move tabulate to main

    return tabulate(relative_select_all(database),
                    headers="keys",
                    tablefmt="mixed_grid",
                    maxcolwidths=15)
