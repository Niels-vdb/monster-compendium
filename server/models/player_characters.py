from typing import Any, Dict

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .creatures import Creature


class PlayerCharacter(Creature):
    """
    Table that holds all pc that are linked to an active or inactive party.
    Table inherits from Creature table.

    Parameters:
        - name (str): The name of the monster.
        - description (str): Description about how the monster looks like (optional).
        - information (str): Notes and extra information about the monster (optional).
        - alive (bool): Boolean check if monster is alive (True), or dead (False).
        - active (bool): Boolean check if the monster is visible for party (True) or not (False).
        - armour_class (int): The armour class the monster has (optional).
        - image (BLOB): An image of the monster (optional).

        - race (int): The race of the creature, FK to id of the race in the races table (optional).
        - subrace (int): The race of the creature, FK to id of the subrace in the subraces table (optional).
        - size_id (int): The size of the creature, FK to id of the size in the sizes table.
        - type_id (int): The type of the creature, FK to id of the type in the types table (optional).
        - user_id (int): The user to whom this character belongs to, FK to the id of the user table.

        - parties (List[Party]): The party(s) this creature belongs to. Linked to actual model, can be multiple (optional).
        - classes (List[Class]): The class(es) the creature belongs to. Linked to actual model (optional).
        - immunities (List[Effect]): The effect(s) the creature is immune to. Linked to actual model (optional).
        - resistances (List[Effect]): The effect(s) the creature is resistance to. Linked to actual model (optional).
        - vulnerabilities (List[Effect]): The effect(s) the creature is vulnerable to. Linked to actual model (optional).
    """

    __tablename__ = "player_characters"
    __mapper_args__ = {"polymorphic_identity": "player_characters"}

    id = Column(Integer, ForeignKey("creatures.id"), primary_key=True)

    # n-1 relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="characters")

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the PCCharacter instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}(id={self.id}, name={self.name!r}, 
            description={self.description!r}, information={self.information!r}, 
            user={self.user}, alive={self.alive}, active={self.active}, 
            armour_class={self.armour_class}, image={self.image}, 
            race={self.race.name if self.race else 'None'}, 
            subrace={self.subrace.name if self.subrace else 'None'}, 
            size={self.size.name if self.size else 'None'}, 
            type={self.creature_type.name if self.creature_type else 'None'}, 
            parties={[party.name for party in self.parties]}, 
            classes={[cls.name for cls in self.classes]}, 
            subclasses={[subclass.name for subclass in self.subclasses]}, 
            immunities={[immunity.name for immunity in self.immunities]}, 
            resistances={[resistance.name for resistance in self.resistances]}, 
            vulnerabilities={[vul.name for vul in self.vulnerabilities]}
            )"""
