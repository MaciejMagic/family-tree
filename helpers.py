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


def start() -> int:
    """ Starting options for the program """

    option = input("""Welcome to Family Tree

Available options:
    1. Add new relative
    2. Modify info about existing relative
    3. Generate tree
    4. List all relatives
    5. Exit
Proceed with: """).strip()

    if option not in [1, 2, 3, 4, 5]:
        raise ValueError("Wrong input")

    return int(option)
