from typing import Any, Dict

from sqlalchemy import BLOB, Boolean, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from .base import Base


class NPCCharacters(Base):
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

    npc_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(Text, nullable=True)
    information = Column(Text, nullable=True)
    alive = Column(Boolean, nullable=False)
    active = Column(Boolean, nullable=False)
    armour_class = Column(Integer, nullable=True)
    image = Column(BLOB, nullable=True)
    race = Column(Integer, ForeignKey("races.race_id"), nullable=False)
    subrace = Column(Integer, ForeignKey("subraces.subrace_id"), nullable=True)

    # Define relationships
    classes = relationship("Classes", secondary="npc_classes")
    immunities = relationship("Effects", secondary="npc_immunities")
    resistances = relationship("Effects", secondary="npc_resistances")
    vulnerabilities = relationship("Effects", secondary="npc_vulnerabilities")

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the NPCCharacter instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}('{self.npc_id}', '{self.name}', 
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
            "npc_id": self.npc_id,
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


# Cross-reference table holding the NPC and its class. If the class has a subclass it will also hold the subclass.
npc_classes = Table(
    "npc_classes",
    Base.metadata,
    Column("npc_id", Integer, ForeignKey("npc_characters.npc_id"), nullable=False),
    Column("class_id", Integer, ForeignKey("classes.class_id"), nullable=False),
    Column("subclass_id", Integer, ForeignKey("subclasses.subclass_id"), nullable=True),
)

# Cross-reference table holding the NPC and its immunities.
npc_immunities = Table(
    "npc_immunities",
    Base.metadata,
    Column("effect_id", Integer, ForeignKey("effects.effect_id"), nullable=False),
    Column("npc_id", Integer, ForeignKey("npc_characters.npc_id"), nullable=False),
)

# Cross-reference table holding the NPC and its resistances.
npc_resistances = Table(
    "npc_resistances",
    Base.metadata,
    Column("effect_id", Integer, ForeignKey("effects.effect_id"), nullable=False),
    Column("npc_id", Integer, ForeignKey("npc_characters.npc_id"), nullable=False),
)

# Cross-reference table holding the NPC and its vunrabilities.
npc_vulnerabilities = Table(
    "npc_vulnerabilities",
    Base.metadata,
    Column("effect_id", Integer, ForeignKey("effects.effect_id"), nullable=False),
    Column("npc_id", Integer, ForeignKey("npc_characters.npc_id"), nullable=False),
)
