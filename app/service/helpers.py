import argparse
import sqlite3
import sys


def arguments() -> argparse.Namespace:
    """
    Command-line arguments and flag handling. Creates a parser object
    with arguments and returns a parsed namespace object.
    """
    parser = argparse.ArgumentParser(
        prog='Family Tree',
        description='Family Tree - a CLI tool for generating a directional graphs',
        epilog='🌳🌳🌳')

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1',
    )

    parser.add_argument(
        '-i',
        '--input',
        action='store_const',
        help='custom input file with database',
        dest='file_input',
        metavar='INPUT_FILE',
        default='../database/tree.db',
    )

    parser.add_argument(
        '-o',
        '--output',
        action='store_const',
        help='outputs to specified file',
        dest='file_output',
        metavar='OUTPUT_FILE',
        default='family_tree.pdf',
    )

    return parser.parse_args()


def connect_to_db(
    database_file: str = "../database/tree.db"
) -> sqlite3.Connection | None:
    """
    Establishes a connection to specified SQLite 3 database.
    Returns a connection object.
    """
    connection = None
    try:
        connection = sqlite3.connect(database_file)
    except (sqlite3.OperationalError, FileNotFoundError):
        sys.exit("Error: cannot connect to database")

    return connection


def start() -> int | None:
    """ Starting options for the program """

    start_usage = "Usage: type a number 1 - 6 and hit ENTER"

    try:
        option = int(input("""\n🌳 Welcome to Family Tree 🌳\n
    Available options:
        1. Add new relative
        2. Modify info about existing relative
        3. Generate tree
        4. List all relatives (less detailed)
        5. List all relatives (more detailed)
        6. Exit
    Proceed with: """).strip())

        if option not in [1, 2, 3, 4, 5, 6]:
            print("Wrong input", file=sys.stderr)
            print(start_usage)
            return None

    except TypeError:
        print("Wrong option", file=sys.stderr)
        print(start_usage)
        return None

    return option
