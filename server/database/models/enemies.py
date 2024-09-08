from typing import Any, Dict

from sqlalchemy import BLOB, Boolean, Column, Integer, String, Table, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Enemy(Base):
    """
    Table that holds all monsters the party has fought along their travels.

    Parameters:
        - name (str): The name of the NPC.
        - description (str): Description about how the monster looks like (optional).
        - information (str): Notes and extra information about the monster (optional).
        - alive (bool): Boolean check if NPC is alive (True), or dead (False).
        - active (bool): Boolean check if the NPC is visible for party (True) or not (False).
        - amour_class (int): The armour class the NPC has (optional).
        - image (BLOB): An image of the NPC (optional).
        - race (int): FK to the "races" table holding the PK of the race of the NPC.
        - subrace (int): FK to the "subraces" table holding the PK of the subrace of the NPC (optional).
    """

    __tablename__ = "enemies"

    enemy_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    information = Column(Text, nullable=True)
    alive = Column(Boolean, nullable=False)
    active = Column(Boolean, nullable=False)
    armour_class = Column(Integer)
    image = Column(BLOB, nullable=True)
    race = Column(Integer, ForeignKey("races.race_id"), nullable=False)
    subrace = Column(Integer, ForeignKey("subraces.subrace_id"), nullable=True)

    # Define relationships
    classes = relationship("Class", secondary="enemy_classes")
    immunities = relationship("Effect", secondary="enemy_immunities")
    resistances = relationship("Effect", secondary="enemy_resistances")
    vulnerabilities = relationship("Effect", secondary="enemy_vulnerabilities")

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Enemies instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}('{self.enemy_id}', '{self.name}',
        '{self.description}', '{self.information}', '{self.alive}',
        '{self.active}', '{self.armour_class}', '{self.image}', '{self.race}',
        '{self.subrace}', '{self.classes}', '{self.immunities}', '{self.resistances}', 
        '{self.vulnerabilities}')"""

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Enemies instance.
        :rtype: Dict[str, Any]
        """
        return {
            "enemy_id": self.enemy_id,
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


class Monster(Base):
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

    monster_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    information = Column(Text, nullable=True)
    alive = Column(Boolean, nullable=False)
    active = Column(Boolean, nullable=False)
    armour_class = Column(Integer, nullable=False)
    image = Column(BLOB, nullable=True)
    size_id = Column(Integer, ForeignKey("sizes.size_id"), nullable=False)
    type_id = Column(Integer, ForeignKey("types.type_id"), nullable=False)

    # Define relationships
    immunities = relationship("Effect", secondary="monster_immunities")
    resistances = relationship("Effect", secondary="monster_resistances")
    vulnerabilities = relationship("Effect", secondary="monster_vulnerabilities")

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Monster instance.
        :rtype: str
        """
        return f"""{self.__class__.__name__}('{self.monster_id}', '{self.name}',
        '{self.description}', '{self.information}', '{self.alive}',
        '{self.active}', '{self.armour_class}', '{self.image}', '{self.type_id}',
        '{self.size_id}', '{self.immunities}', '{self.resistances}', 
        '{self.vulnerabilities}')"""

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Monster instance.
        :rtype: Dict[str, Any]
        """
        return {
            "monster_id": self.monster_id,
            "name": self.name,
            "description": self.description,
            "information": self.information,
            "alive": self.alive,
            "active": self.active,
            "armour_class": self.armour_class,
            "image": self.image,
            "type": self.type_id,
            "size": self.size_id,
            "immunities": [imm.to_dict() for imm in self.immunities],
            "resistances": [res.to_dict() for res in self.resistances],
            "vulnerabilities": [vul.to_dict() for vul in self.vulnerabilities],
        }


class Type(Base):
    """

    Parameters:
        - type (str): The name of the type
    """

    __tablename__ = "types"

    type_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    def __repr__(self) -> str:
        """
        This method provides a readable string of the instance including all
        its attributes.

        :returns: A string representation of the Types instance.
        :rtype: str
        """
        return f"{self.__class__.__tablename__}('{self.type_id}', '{self.name}')"

    def to_dict(self) -> Dict[str, Any]:
        """
        This method creates a dictionary where the keys are attribute names and
        the values are the attribute values, facilitating data serialization.

        :returns: A dictionary representation of the Types instance.
        :rtype: Dict[str, Any]
        """
        return {"type_id": self.type_id, "type": self.name}


# Cross-reference table for enemies and their classes
enemy_classes = Table(
    "enemy_classes",
    Base.metadata,
    Column("enemy_id", Integer, ForeignKey("enemies.enemy_id"), nullable=False),
    Column("class_id", Integer, ForeignKey("classes.class_id"), nullable=False),
    Column("subclass_id", Integer, ForeignKey("subclasses.subclass_id"), nullable=True),
)

# Cross-reference table for enemies and their immunities
enemy_immunities = Table(
    "enemy_immunities",
    Base.metadata,
    Column("effect_id", Integer, ForeignKey("effects.effect_id"), nullable=False),
    Column("enemy_id", Integer, ForeignKey("enemies.enemy_id"), nullable=False),
)

# Cross-reference table for enemies and their resistances
enemy_resistances = Table(
    "enemy_resistances",
    Base.metadata,
    Column("effect_id", Integer, ForeignKey("effects.effect_id"), nullable=False),
    Column("enemy_id", Integer, ForeignKey("enemies.enemy_id"), nullable=False),
)

# Cross-reference table for enemies and their vulnerabilities
enemy_vulnerabilities = Table(
    "enemy_vulnerabilities",
    Base.metadata,
    Column("effect_id", Integer, ForeignKey("effects.effect_id"), nullable=False),
    Column("enemy_id", Integer, ForeignKey("enemies.enemy_id"), nullable=False),
)

monster_immunities = Table(
    "monster_immunities",
    Base.metadata,
    Column("monster_id", Integer, ForeignKey("monsters.monster_id"), nullable=False),
    Column("effect_id", Integer, ForeignKey("effects.effect_id"), nullable=False),
)

monster_resistances = Table(
    "monster_resistances",
    Base.metadata,
    Column("monster_id", Integer, ForeignKey("monsters.monster_id"), nullable=True),
    Column("effect_id", Integer, ForeignKey("effects.effect_id"), nullable=True),
)

monster_vulnerabilities = Table(
    "monster_vulnerabilities",
    Base.metadata,
    Column("monster_id", Integer, ForeignKey("monsters.monster_id"), nullable=True),
    Column("effect_id", Integer, ForeignKey("effects.effect_id"), nullable=True),
)
