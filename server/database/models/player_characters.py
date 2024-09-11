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
        - amour_class (int): The armour class the monster has (optional).
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

    __tablename__ = "pc_characters"
    __mapper_args__ = {"polymorphic_identity": "pc_characters"}

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
        return f"""{self.__class__.__name__}('{self.id}', '{self.name}',
        '{self.description}', '{self.information}', '{self.alive}',
        '{self.active}', '{self.armour_class}', '{self.image}', '{self.race}',
        '{self.subrace}', '{self.user_id}', '{self.classes}', '{self.immunities}',
        '{self.resistances}', '{self.vulnerabilities}')"""

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the PCCharacter instance.
        :rtype: Dict[str, Any]
        """
        return {
            "pc_id": self.id,
            "name": self.name,
            "description": self.description,
            "information": self.information,
            "alive": self.alive,
            "active": self.active,
            "armour_class": self.armour_class,
            "image": self.image,
            "race": self.race,
            "subrace": self.subrace,
            "user_id": self.user_id,
            "classes": [cls.to_dict() for cls in self.classes],
            "immunities": [imm.to_dict() for imm in self.immunities],
            "resistances": [res.to_dict() for res in self.resistances],
            "vulnerabilities": [vul.to_dict() for vul in self.vulnerabilities],
        }
