from typing import Any, Dict

from sqlalchemy import Column, Integer, ForeignKey

from .creatures import Creature


class Monster(Creature):
    """
    Table that holds all monsters the party has fought along their travels.
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

        - parties (List[Party]): The party(s) this creature belongs to. Linked to actual model, can be multiple (optional).
        - classes (List[Class]): The classes the creature belongs to, can be multiple (optional).
        - immunities (List[Effect]): The effects the creature is immune to, can be multiple (optional).
        - resistances (List[Effect]): The effects the creature is resistance to, can be multiple (optional).
        - vulnerabilities (List[Effect]): The effects the creature is vulnerable to, can be multiple (optional).
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
            '{self.active}', '{self.armour_class}', '{self.image}', 
            '{self.race}', '{self.subrace}', '{self.size}', '{self.type_id}', 
            '{self.parties}', '{self.classes}', '{self.subclasses}', 
            '{self.immunities}', '{self.resistances}', '{self.vulnerabilities}')"""

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Monster instance.
        :rtype: Dict[str, Any]
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "information": self.information,
            "alive": self.alive,
            "active": self.active,
            "armour_class": self.armour_class,
            "image": self.image,
            "race": self.race,
            "subrace": self.subrace,
            "size": self.size,
            "type": self.type_id,
            "parties": self.parties,
            "classes": [cls.to_dict() for cls in self.classes],
            "subclasses": [subcls.to_dict() for subcls in self.subclasses],
            "immunities": [imm.to_dict() for imm in self.immunities],
            "resistances": [res.to_dict() for res in self.resistances],
            "vulnerabilities": [vul.to_dict() for vul in self.vulnerabilities],
        }
