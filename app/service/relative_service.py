import sqlite3
import sys

from model.relative import FEATURES, Relative
from tabulate import tabulate

SQL_INSERT = """INSERT INTO family
                (first_name, last_name, gender, family_name, date_of_birth,
                place_of_birth, date_of_death, place_of_death, phone, email,
                events, desc, spouse, children)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

SQL_SELECT = """SELECT * FROM family
                WHERE first_name = ? AND last_name = ?
                ORDER BY date_of_birth ASC"""

SQL_SELECT_ALL = """SELECT * FROM family
                    ORDER BY date_of_birth ASC"""

SQL_DELETE = "DELETE FROM family WHERE id = ?"


def relative_new(cursor: sqlite3.Cursor) -> Relative | None:
    """
    Collects input for each attribute from user.
    Creates and returns a new Relative object.
    """

    try:
        print("Provide info for a new person: ('Enter' to skip)")
        relative_new_person = Relative()
        for feature in FEATURES:
            feature_value = input(f"{feature.replace('_', ' ').title()}: ")
            try:
                setattr(relative_new_person, feature, feature_value)
            except ValueError:
                print("Input value error")
                setattr(relative_new_person, feature, None)

        answer = input("Is the provided information correct? [Y/N] ") \
            .strip() \
            .lower()
        if answer == "y":
            result = relative_new_save(relative_new_person, cursor)
            if result in [1, 2, 3]:
                print("Adding new person unsuccessful")
                return None
            print("New relative (" + relative_new_person.first_name +
                  " " + relative_new_person.last_name + ") saved")
            return relative_new_person
        else:
            print("Info discarded")
            return None

    except AttributeError:
        print("Attribute value error. Info discarded")
        return None


def relative_new_save(person: Relative, cursor: sqlite3.Cursor) -> int:
    """
    Persists a Relative object as a row in database.
    """

    matches = relative_load(cursor, first_name=person.first_name,
                            last_name=person.last_name)

    feedback = f"Relative info ({person.first_name} {person.last_name}) saved successfully"

    if matches:
        print("Following people already exist with provided name:")
        for match in matches:
            print("- id:", match['id'], ", ", match['first_name'], " ",
                  match['last_name'], ", born ", match['date_of_birth'])

        answer = input("Add new person with the same credentials? [Y/N] ") \
            .strip() \
            .lower()
        if answer == "y":
            pass
        else:
            print("Action cancelled")
            return 1

    try:
        insert = cursor.execute(SQL_INSERT,
                                (person.first_name,
                                 person.last_name,
                                 person.gender,
                                 person.family_name,
                                 person.date_of_birth,
                                 person.place_of_birth,
                                 person.date_of_death,
                                 person.place_of_death,
                                 person.phone,
                                 person.email,
                                 person.events,
                                 person.desc))
        cursor.connection.commit()
    except FileNotFoundError:
        print("Error: database file not found")
        return 2
    except sqlite3.Error:
        print("Error writing to database")
        return 3

    if insert:
        print(feedback)
    return 0


def relative_load(cursor: sqlite3.Cursor, **kwargs) -> list[Relative] | None:
    """
    Returns a list of Relative objects specified by first_name
    and last_name keywords, loaded from database.
    """

    try:
        results = cursor.execute(SQL_SELECT,
                                 (kwargs["first_name"],
                                  kwargs["last_name"])).fetchall()
    except sqlite3.Error:
        print("Error: loading from database", file=sys.stderr)

    if results:
        return list(map(lambda match: Relative(**match), results))

    return None


def relative_select_all(cursor: sqlite3.Cursor) -> list[dict] | None:
    """ Selects all rows in database. Returns a list of dictionaries """

    try:
        results = cursor.execute(SQL_SELECT_ALL).fetchall()
    except sqlite3.Error:
        print("Error: loading all entries from database", file=sys.stderr)

    if results:
        return results
    return None


def relative_mod_attr(person: Relative, info: int, content: str) -> Relative:
    """
    Modifies an attribute in a Relative object.
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


def relative_modify(cursor: sqlite3.Cursor, first_name: str, last_name: str) -> None:
    """
    Modifies an existing person in database.
    """

    # Search for list of matches
    relatives_loaded = relative_load(
        cursor, first_name=first_name, last_name=last_name)

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
    relative_update(cursor, person_edited)

    print("Modified info (" + person_to_edit.first_name +
          " " + person_to_edit.last_name + ") saved")


def relative_update(cursor: sqlite3.Cursor, person: Relative) -> None:
    """
    Updates existing row in database through data from a Relative object.
    """

    for feature in FEATURES:
        value = getattr(person, feature)

        update_sql = f"UPDATE family SET {feature} = {value} WHERE id = ?"

        try:
            cursor.execute(update_sql, (person.id,))
            cursor.connection.commit()
        except sqlite3.Error:
            print("Error: updating to database", file=sys.stderr)
        except FileNotFoundError:
            print("Error: database file not found", file=sys.stderr)

        print(f"{feature.replace('_', ' ').title()} update successful")


def relative_delete(cursor: sqlite3.Cursor, person: Relative) -> None:
    """
    Removes an existing person from database.
    """

    try:
        if person.id is None:
            print("Error: deletion unsuccessful - no object ID")
            return
        delete = cursor.execute(SQL_DELETE, (person.id,))
        cursor.connection.commit()
    except sqlite3.Error:
        print("Deletion error with database", file=sys.stderr)

    if delete:
        print("Deletion successful")
    else:
        print("Deletion unsuccessful")
    return


def relatives_show_less(cursor: sqlite3.Cursor) -> str | None:
    """
    Retrieves all entries from database and prints basic info.
    """

    results = relative_select_all(cursor)

    if results:
        return str([(person["first_name"]
                     + " "
                     + person["last_name"]
                     + " ("
                     + person["date_of_birth"]
                     + " - "
                     + person["date_of_death"]
                     + ")"
                     + "\n") for person in results])
    return None


def relative_show_more(cursor: sqlite3.Cursor) -> str:
    """
    Retrieves all entries from database.
    Returns a multiline string formatted as a table.
    """

    return tabulate(relative_select_all(cursor),
                    headers="keys",
                    tablefmt="mixed_grid",
                    maxcolwidths=15)
