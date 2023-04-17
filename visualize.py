import sys
import csv
import sqlite3
import graphviz
from main import connect_to_db


def generate_tree_csv(input_file: str) -> None:
    """
    Generates a svg file with a graph tree from a csv file
    """
    with open(input_file, "r", encoding="UTF-8") as file:
        try:
            tree = graphviz.Digraph(comment="Family Tree")
            reader = csv.DictReader(file)

            for person in reader:
                tree.node(
                    str(person[id]), f"{person['first_name']} {person['last_name']}")
                # tree.edge()
                # TO DO

            tree.render("output/tree.gv").replace("\\", "/")
            tree.render("output/tree.gv", view=True)

        except (ValueError, TypeError, FileNotFoundError, NameError):
            sys.exit("Invalid file")


def generate_tree_db(*args) -> None:
    """
    Generates a svg file with a graph tree from database records
    """
    # TO DO - sqlite db reader - iterate through records
    if len(args) == 1:
        with open(args[0], "r", encoding="UTF-8") as file:
            try:
                tree = graphviz.Digraph(comment="Family Tree")
                people = []
                # Initialize database
                db_connection = connect_to_db(file)
                selection = db_connection.execute("SELECT * FROM family")
                for person in selection:
                    tree.node(
                        str(person[id]), f"{person['first_name']} {person['last_name']}")

                tree.render("output/tree.gv").replace("\\", "/")
                tree.render("output/tree.gv", view=True)

            except FileNotFoundError:
                sys.exit("File not found")

    elif len(args) == 0:
        with open("tree.db", "r", encoding="UTF-8") as file:
            try:
                tree = graphviz.Digraph(comment="Family Tree")
                people = []
                # Initialize database
                db_connection = connect_to_db(file)
                selection = db_connection.execute("SELECT * FROM family")
                for person in selection:
                    tree.node(
                        str(person[id]), f"{person['first_name']} {person['last_name']}")

                tree.render("output/tree.gv").replace("\\", "/")
                tree.render("output/tree.gv", view=True)

            except FileNotFoundError:
                sys.exit("File not found")

    else:
        raise ValueError
