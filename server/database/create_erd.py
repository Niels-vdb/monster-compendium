from eralchemy2 import render_er

from server.database.models.base import Base


def create_erd() -> None:
    """
    Uses the eralchemy2, graphviz and pygraphviz packages to create ERDiagrams from
    the ORM classes created using SQLAlchemy.
    """
    render_er(input=Base.metadata, output="docs/diagrams/erd.png")


if __name__ == "__main__":
    create_erd()
