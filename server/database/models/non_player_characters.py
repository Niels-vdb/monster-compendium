from typing import Any, Dict

from sqlalchemy import Column, ForeignKey, Integer
from .creatures import Creature


class NonPlayerCharacter(Creature):
    """
    Table that holds all noticeable NPC's the party has met along their travels.
    Table inherits from Creature table.

    Parameters:
        - name (str): The name of the monster.
        - description (str): Description about how the monster looks like (optional).
        - information (str): Notes and extra information about the monster (optional).
        - alive (bool): Boolean check if monster is alive (True), or dead (False).
        - active (bool): Boolean check if the monster is visible for party (True) or not (False).
        - armour_class (int): The armour class the monster has (optional).
        - image (BLOB): An image of the monster (optional).

        - race (int): The race of the creature, FK to id of the races table (optional).
        - subrace (int): The race of the creature, FK to id of the subraces table (optional).
        - size_id (int): The size of the creature, FK to id of the sizes table.
        - type_id (int): The type of the creature, FK to id of the types table (optional).

        - parties (list[Party]): The party(s) this creature belongs to. Linked to actual model, can be multiple (optional).
        - classes (list[Class]): The classes the creature belongs to, can be multiple (optional).
        - immunities (list[Effect]): The effects the creature is immune to, can be multiple (optional).
        - resistances (list[Effect]): The effects the creature is resistance to, can be multiple (optional).
        - vulnerabilities (list[Effect]): The effects the creature is vulnerable to, can be multiple (optional).
    """

    __tablename__ = "non_player_characters"
    __mapper_args__ = {"polymorphic_identity": "non_player_characters"}

    id = Column(Integer, ForeignKey("creatures.id"), primary_key=True)
