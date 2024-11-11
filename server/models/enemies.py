from sqlalchemy import Column, Integer, ForeignKey

from .creatures import Creature


class Enemy(Creature):
    """
    Table that holds all enemies the party has fought along their travels.
    Table inherits from Creature table.

    Parameters:
        - name (str): The name of the enemy.
        - description (str): Description about how the enemy looks like (optional).
        - information (str): Notes and extra information about the enemy (optional).
        - alive (bool): Boolean check if enemy is alive (True), or dead (False).
        - active (bool): Boolean check if the enemy is visible for party (True) or not (False).
        - armour_class (int): The armour class the enemy has (optional).
        - image (BLOB): An image of the enemy (optional).

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

    __tablename__ = "enemies"
    __mapper_args__ = {"polymorphic_identity": "enemies"}

    id = Column(Integer, ForeignKey("creatures.id"), primary_key=True)
