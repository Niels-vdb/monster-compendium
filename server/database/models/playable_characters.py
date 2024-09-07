from typing import Any, Dict

from sqlalchemy import BLOB, Boolean, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from .base import Base


class PlayableCharacters(Base):
    __tablename__ = "playable_characters"

    pc_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(Text, nullable=True)
    information = Column(Text, nullable=True)
    alive = Column(Boolean, nullable=False)
    active = Column(Boolean, nullable=False)
    armour_class = Column(Integer)
    image = Column(BLOB, nullable=True)
    race = Column(Integer, ForeignKey("races.race_id"), nullable=False)
    subrace = Column(Integer, ForeignKey("subraces.subrace_id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # Define relationships
    classes = relationship("Classes", secondary="pc_classes")
    immunities = relationship("Effects", secondary="pc_immunities")
    resistances = relationship("Effects", secondary="pc_resistances")
    vulnerabilities = relationship("Effects", secondary="pc_vulnerabilities")

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the PCCharacter instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}('{self.pc_id}', '{self.name}',
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
            "pc_id": self.pc_id,
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


# Cross-reference table holding the PC and its class. If the class has a subclass it will also hold the subclass.
PCClasses = Table(
    "pc_classes",
    Base.metadata,
    Column("pc_id", Integer, ForeignKey("playable_characters.pc_id"), nullable=False),
    Column("class_id", Integer, ForeignKey("classes.class_id"), nullable=False),
    Column("subclass_id", Integer, ForeignKey("subclasses.subclass_id"), nullable=True),
)

# Cross-reference table holding the PC and its immunities.
PCImmunities = Table(
    "pc_immunities",
    Base.metadata,
    Column("pc_id", Integer, ForeignKey("playable_characters.pc_id"), nullable=False),
    Column("effect_id", Integer, ForeignKey("effects.effect_id"), nullable=False),
)

# Cross-reference table holding the PC and its resistances.
PCResistances = Table(
    "pc_resistances",
    Base.metadata,
    Column("pc_id", Integer, ForeignKey("playable_characters.pc_id"), nullable=False),
    Column("effect_id", Integer, ForeignKey("effects.effect_id"), nullable=False),
)

# Cross-reference table holding the PC and its vunrabilities.
PCVulnerabilities = Table(
    "pc_vulnerabilities",
    Base.metadata,
    Column("pc_id", Integer, ForeignKey("playable_characters.pc_id"), nullable=False),
    Column("effect_id", Integer, ForeignKey("effects.effect_id"), nullable=False),
)
