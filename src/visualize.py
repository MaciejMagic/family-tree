import sqlite3
import sys

import graphviz
from src.relative_service import relative_select_all


def generate_tree(
        database: sqlite3.Connection = None,
        input_file: str = "db/tree.db"
) -> None:
    """ Generates a svg graph file of a tree from database """

    with open(input_file, "r", encoding="UTF-8") as file:
        try:
            # Initialize graph object
            tree = graphviz.Digraph(comment="Family Tree")

            # Import list of dicts (relatives) from database
            relatives = relative_select_all(database)

            # Generate tree nodes
            for person in relatives:
                shape = "rect" if person["gender"] == "male" else "ellipse"
                tree.node(
                    str(person["id"]),
                    f"{person['first_name']} {person['last_name']}",
                    tooltip=f"{person['date_of_birth']} - {person['date_of_death']}",
                    shape=shape
                )

            # TODO -Generate tree edges

            # Generate output file
            tree.render("output/tree.gv").replace("\\", "/")
            tree.render("output/tree.gv", view=True)

        except FileNotFoundError:
            sys.exit("File not found")
