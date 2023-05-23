import sys

import graphviz
from helpers import connect_to_db


def generate_tree(input_file: str = "tree.db") -> None:
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
