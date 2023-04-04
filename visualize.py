import sys
import csv
import graphviz


def generate_tree_csv():
    """
    Generates a svg file with a graph tree from a csv file
    """
    dot = graphviz.Digraph(comment="Family Tree")

    with open(sys.argv[1]) as file:
        try:
            people = []
            reader = csv.reader(file)
            for row in reader:
                node = dot.node(people[row], f"{first_name} {last_name}")
                dot.edge(people[row], x)

        except (ValueError, TypeError, FileNotFoundError, NameError):
            sys.exit("Invalid file")


def generate_tree_db():
    """
    Generates a svg file with a graph tree from database records
    """
    pass
