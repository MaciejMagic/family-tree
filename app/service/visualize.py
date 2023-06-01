import sqlite3
import sys

import graphviz
from app.service.relative_service import relative_select_all


def generate_node(tree: graphviz.Digraph, person: dict) -> None:
    """ Creates a node for specified tree (Digraph object) """

    shape = "rect" if person["gender"] == "male" else "ellipse"
    tree.node(
        str(person["id"]),
        f"{person['first_name']} {person['last_name']}",
        tooltip=f"{person['date_of_birth']} - {person['date_of_death']}",
        shape=shape
    )


def generate_tree(database: sqlite3.Connection) -> None:
    """ Generates a svg graph file of a tree from database """

    try:
        # Initialize graph object
        tree = graphviz.Digraph(comment="Family Tree")

        # Import list of Relatives (as dicts) from database
        relatives = relative_select_all(database)

        # Generate first tree node
        previous_person = relatives[0]
        generate_node(tree, previous_person)

        # Generate the rest of tree nodes
        for person in relatives[1:]:
            generate_node(tree, person)

            # Generate tree edge
            tree.edge(f"{previous_person['id']}", f"{person['id']}")

            previous_person = person

        # Generate output file
        tree.render("output/tree.gv").replace("\\", "/")
        tree.render("output/tree.gv", view=True)

    except FileNotFoundError:
        sys.exit("File not found")
