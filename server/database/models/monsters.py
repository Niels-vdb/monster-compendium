from typing import Any, Dict

from sqlalchemy import BLOB, Boolean, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, Creature


class Monster(Creature):
    """
    Table that holds all monsters the party has fought along their travels.

    Parameters:
        - name (str): The name of the monster.
        - description (str): Description about how the monster looks like (optional).
        - information (str): Notes and extra information about the monster (optional).
        - alive (bool): Boolean check if monster is alive (True), or dead (False).
        - active (bool): Boolean check if the monster is visible for party (True) or not (False).
        - amour_class (int): The armour class the monster has (optional).
        - image (BLOB): An image of the monster (optional).
        - size_id (int): FK to the "sizes" table.
        - type_id (int): FK to the "types" table.
    """

    __tablename__ = "monsters"
    __mapper_args__ = {"polymorphic_identity": "monsters"}

    id = Column(Integer, ForeignKey("creatures.id"), primary_key=True)

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Monster instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}('{self.id}', '{self.name}',
        '{self.description}', '{self.information}', '{self.alive}',
        '{self.active}', '{self.armour_class}', '{self.image}', '{self.type_id}',
        '{self.size}', '{self.immunities}', '{self.resistances}',
        '{self.vulnerabilities}')"""

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Monster instance.
        :rtype: Dict[str, Any]
        """
        return {
            "monster_id": self.id,
            "name": self.name,
            "description": self.description,
            "information": self.information,
            "alive": self.alive,
            "active": self.active,
            "armour_class": self.armour_class,
            "image": self.image,
            "type": self.type_id,
            "sizes": self.size,
            "immunities": [imm.to_dict() for imm in self.immunities],
            "resistances": [res.to_dict() for res in self.resistances],
            "vulnerabilities": [vul.to_dict() for vul in self.vulnerabilities],
        }
