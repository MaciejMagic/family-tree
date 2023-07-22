import sqlite3
import sys
from pathlib import Path

from model.relative import FEATURES, FamilyRelative
from tabulate import tabulate


def read_sql_query(sql_path: Path) -> str:
    """Returns content of an SQL file as a string"""
    return Path(sql_path).read_text(encoding="UTF-8")


def relative_create(cursor: sqlite3.Cursor) -> FamilyRelative | None:
    """
    Collects input for each attribute from user.
    Creates and returns a new Relative object.
    """
    try:
        print("Provide info for a new person: ('Enter' to skip)")
        relative_new_person = FamilyRelative()
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
            result = relative_save(relative_new_person, cursor)
            if result in [1, 2, 3]:
                print("Adding new person unsuccessful")
                return None
            print("New relative (" + relative_new_person.first_name +
                  " " + relative_new_person.last_name + ") saved")
            return relative_new_person
        print("Info discarded")
        return None

    except AttributeError:
        print("Attribute value error. Info discarded")
        return None


def relative_save(person: FamilyRelative, cursor: sqlite3.Cursor) -> int:
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
        sql_query = read_sql_query("../sql/insert.sql")
        insert = cursor.execute(sql_query,
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


def relative_load(cursor: sqlite3.Cursor, **kwargs) -> list[FamilyRelative] | None:
    """
    Returns a list of Relative objects specified by first_name
    and last_name keywords, loaded from database.
    """
    try:
        sql_query = read_sql_query("../sql/select.sql")
        results = cursor.execute(sql_query,
                                 (kwargs["first_name"],
                                  kwargs["last_name"])).fetchall()
    except sqlite3.Error:
        print("Error: loading from database", file=sys.stderr)

    if results:
        return list(map(lambda match: FamilyRelative(**match), results))
    return None


def relative_select_all(cursor: sqlite3.Cursor) -> list[dict] | None:
    """ Selects all rows in database. Returns a list of dictionaries """
    try:
        sql_query = read_sql_query("../sql/select_all.sql")
        results = cursor.execute(sql_query).fetchall()
    except sqlite3.Error:
        print("Error: loading entries from database", file=sys.stderr)

    if results:
        return results
    return None


def relative_modify_attr(person: FamilyRelative, info: int, content: str) -> FamilyRelative:
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


def relative_find(relatives: list[FamilyRelative]) -> FamilyRelative | None:
    """
    Takes a list of Relative objects as an argument, asks for user input
    and returns a single Relative object or None.
    """

    # If there are multiple people with the given name, list them
    found = len(relatives)
    if found > 1:
        for person in relatives:
            list_item = str(
                ((len(relatives) + 1) - found), '. ',
                person.first_name, ' ', person.last_name,
                ', born ', person.date_of_birth
            )
            print(list_item)
            found -= 1
        while True:
            try:
                # Ask which entry to edit
                person_choice = int(
                    input("\nWhich person to edit (type number and hit Enter): ").strip())
                break
            except TypeError:
                print("Wrong input. Try again.")

        person_to_edit = relatives[person_choice - 1]

    elif relatives is None:
        print("Error: list of Relatives is empty")
        return None
    else:
        person_to_edit = relatives[0]

    return person_to_edit


def relative_modify(cursor: sqlite3.Cursor, relatives: list[FamilyRelative]) -> str:
    """
    Modifies an existing person in database. Requires a cursor object
    and a list of Relative objects. Collects user input for modification.
    Returns confirmation info as a string.
    """
    person_to_edit = relative_find(relatives)

    if person_to_edit is None:
        return "Error: no relative to edit"

    while True:
        try:
            # Ask which info to edit
            info_to_edit = int(input("""📄 Which info to add / edit:
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
            break
        except (TypeError, ValueError):
            print("Wrong input. Try again.")

    # Ask with what new content to edit
    new_content = input("Enter new info: ").strip()

    if new_content is None or new_content == "":
        return "Error: no new content provided"

    person_edited = relative_modify_attr(
        person_to_edit,
        info_to_edit,
        new_content
    )

    # Save updated person (row) to database
    relative_update(cursor, person_edited)

    return ("Modified info (" + person_to_edit.first_name +
            " " + person_to_edit.last_name + ") saved successfully\n")


def relative_update(cursor: sqlite3.Cursor, person: FamilyRelative) -> None:
    """
    Updates existing row in database through data from a Relative object.
    """
    for feature in FEATURES:
        value = getattr(person, feature)

        sql_query = read_sql_query("../sql/update.sql")

        try:
            cursor.execute(sql_query, (feature, value, person.id))
            cursor.connection.commit()
        except sqlite3.Error:
            print("Error: updating to database", file=sys.stderr)
        except FileNotFoundError:
            print("Error: database file not found", file=sys.stderr)

        print(f"{feature.replace('_', ' ').title()} updated successfully.")


def relative_delete(cursor: sqlite3.Cursor, person: FamilyRelative) -> None:
    """
    Removes an existing person from database.
    """
    try:
        if person.id is None:
            print("Error: deletion unsuccessful - no object ID")
            return
        sql_query = read_sql_query("../sql/delete.sql")
        delete = cursor.execute(sql_query, (person.id,))
        cursor.connection.commit()
    except sqlite3.Error:
        print("Deletion error with database", file=sys.stderr)

    if delete:
        print("Deletion successful")
    else:
        print("Deletion unsuccessful")
    return


def relatives_show(cursor: sqlite3.Cursor, show_all: bool = False) -> str:
    """
    Retrieves all entries from database as list of dicts.
    Returns a multiline string formatted as a table.
    """
    relatives_loaded = relative_select_all(cursor)

    if relatives_loaded:
        if show_all is True:
            try:
                return tabulate(relatives_loaded,
                                headers="keys",
                                tablefmt="mixed_grid",
                                maxcolwidths=15)
            except IndexError:
                return "Error: tabulate / indexing data"
        else:
            return str([(person["first_name"]
                        + " "
                        + person["last_name"]
                        + " ("
                        + person["date_of_birth"]
                        + " - "
                        + person["date_of_death"]
                        + ")"
                        + "\n") for person in relatives_loaded])

    return "Database empty.\nTry adding new relatives.\n"
