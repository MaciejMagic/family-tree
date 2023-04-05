import sys
import csv
import sqlite3
import graphviz


def generate_tree_csv(input_file):
    """
    Generates a svg file with a graph tree from a csv file
    """
    dot = graphviz.Digraph(comment="Family Tree")

    with open(input_file, "r", encoding="UTF-8") as file:
        try:
            people = []
            reader = csv.reader(file)
            for row in reader:
                node = dot.node(
                    people[row], f"{row['first_name']} {row['last_name']}")
                dot.edge(people[row], xxx)
                # TO DO

        except (ValueError, TypeError, FileNotFoundError, NameError):
            sys.exit("Invalid file")


def generate_tree_db(database):
    """
    Generates a svg file with a graph tree from database records
    """
    # TO DO - sqlite db reader - iterate through records
    pass
