import csv
import sys

import graphviz
from helpers import connect_to_db


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
                # TODO -Generate tree edges

            tree.render("output/tree.gv").replace("\\", "/")
            tree.render("output/tree.gv", view=True)

        except (ValueError, TypeError, FileNotFoundError, NameError):
            sys.exit("Invalid file")


def generate_tree_db(input_file: str) -> None:
    """
    Generates a svg graph file of a tree from database
    """

    with open(input_file, "r", encoding="UTF-8") as file:
        try:
            # Initialize graph object
            tree = graphviz.Digraph(comment="Family Tree")

            # Initialize database
            db_connection = connect_to_db(file)
            selection = db_connection.execute("SELECT * FROM family")

            # Generate tree nodes
            for person in selection:
                tree.node(
                    str(person[id]), f"{person['first_name']} {person['last_name']}")

            # TODO -Generate tree edges

            # Generate output file
            tree.render("output/tree.gv").replace("\\", "/")
            tree.render("output/tree.gv", view=True)

        except FileNotFoundError:
            sys.exit("File not found")
