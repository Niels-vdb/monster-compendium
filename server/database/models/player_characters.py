from typing import Any, Dict

from sqlalchemy import BLOB, Boolean, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from .base import Base, Creature


class PlayerCharacter(Creature):
    __tablename__ = "pc_characters"
    __mapper_args__ = {"polymorphic_identity": "pc_characters"}

    id = Column(Integer, ForeignKey("creatures.id"), primary_key=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    parties = relationship(
        "Party",
        secondary="character_parties",
        back_populates="characters",
    )

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
