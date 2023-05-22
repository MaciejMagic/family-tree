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
