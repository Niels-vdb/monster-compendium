from eralchemy2 import render_er

from server.database.models.base import Base


def create_erd():
    """
    Uses the eralchemy2 package to create ERD's from the ORM classes
    """
    render_er(input=Base.metadata, output="docs/diagrams/erd.png")


create_erd()
