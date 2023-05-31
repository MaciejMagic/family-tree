import argparse
import sqlite3
import sys


def arguments() -> argparse.Namespace:
    """ Command-line argument and flag handling """

    parser = argparse.ArgumentParser(
        description="CLI tool for generating a family tree as a svg/pdf graphic")

    parser.add_argument(
        '-h',
        '--help',
        help='show this message',
        required='False'
    )

    parser.add_argument(
        '-i',
        '--input',
        help='custom input file with database',
        default='tree.db',
        required='False'
    )

    parser.add_argument(
        '-o',
        '--output',
        help='outputs to this file',
        default='family_tree.pdf',
        required='False'
    )

    return parser.parse_args()


def connect_to_db(database: str = "db/tree.db") -> sqlite3.Connection | None:
    """
    Establishes a connection to specified SQLite 3 database
    """

    connection = None
    try:
        connection = sqlite3.connect(database)
    except FileNotFoundError:
        sys.exit("Databse file not found")

    return connection


def start() -> int | None:
    """ Starting options for the program """

    try:
        option = input("""🌳 Welcome to Family Tree 🌳

    Available options:
        1. Add new relative
        2. Modify info about existing relative
        3. Generate tree
        4. List all relatives (less detailed)
        5. List all relatives (more detailed)
        6. Exit
    Proceed with: """).strip()

        if int(option) not in [1, 2, 3, 4, 5, 6]:
            print("Wrong input", file=sys.stderr)
            print("Usage: type a number between 1 - 6, followed by ENTER")
            return None

    except TypeError:
        print("Wrong option", file=sys.stderr)
        print("Usage: type a number between 1 - 6, followed by ENTER")
        return None

    return int(option)
