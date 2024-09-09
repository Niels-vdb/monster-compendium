from typing import Any, Dict

from sqlalchemy import BLOB, Boolean, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from .base import Base, Creature


class NPCCharacter(Creature):
    """
    Table that holds all noticeable NPC's the party has met along their travels.

    Parameters:
        - name (str): The name of the NPC.
        - description (str): Description about how the NPC looks like (optional).
        - information (str): Notes and extra information about the NPC (optional).
        - alive (bool): Boolean check if NPC is alive (True), or dead (False).
        - amour_class (int): The armour class the NPC has (optional).
        - active (bool): Boolean check if the NPC is visible for party (True) or not (False).
        - image (BLOB): An image of the NPC (optional).
        - race (int): FK to the "races" table holding the PK of the race of the NPC.
        - subrace (int): FK to the "subraces" table holding the PK of the subrace of the NPC (optional).
    """

    __tablename__ = "npc_characters"
    __mapper_args__ = {"polymorphic_identity": "npc_characters"}

    id = Column(Integer, ForeignKey("creatures.id"), primary_key=True)

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the NPCCharacter instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}('{self.id}', '{self.name}',
        '{self.description}', '{self.information}', '{self.alive}', '{self.active}',
        '{self.armour_class}', '{self.image}', '{self.race}', '{self.subrace}',
        '{self.classes}', '{self.immunities}', '{self.resistances}',
        '{self.vulnerabilities}')"""

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the NPCCharacter instance.
        :rtype: Dict[str, Any]
        """
        return {
            "npc_id": self.id,
            "name": self.name,
            "description": self.description,
            "information": self.information,
            "alive": self.alive,
            "active": self.active,
            "armour_class": self.armour_class,
            "image": self.image,
            "race": self.race,
            "subrace": self.subrace,
            "classes": [cls.to_dict() for cls in self.classes],
            "immunities": [imm.to_dict() for imm in self.immunities],
            "resistances": [res.to_dict() for res in self.resistances],
            "vulnerabilities": [vul.to_dict() for vul in self.vulnerabilities],
        }
