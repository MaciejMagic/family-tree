import sqlite3
import sys


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
    -h, --help      show this help

""")


def connect_to_db(database: str = "tree.db") -> sqlite3.Connection | None:
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
        option = input("""Welcome to Family Tree

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
            return None

    except TypeError:
        print("Wrong option", file=sys.stderr)
        return None

    return int(option)
