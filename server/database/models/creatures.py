from sqlalchemy import BLOB, Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base


class Creature(Base):
    """
    Base table all creature types inherit from.

    Parameters:
        - name (str): The name of the monster.
        - description (str): Description about how the monster looks like (optional).
        - information (str): Notes and extra information about the monster (optional).
        - alive (bool): Boolean check if monster is alive (True), or dead (False).
        - active (bool): Boolean check if the monster is visible for party (True) or not (False).
        - amour_class (int): The armour class the monster has (optional).
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

    __tablename__ = "creatures"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    information = Column(Text, nullable=True)
    alive = Column(Boolean, nullable=False, default=True)
    active = Column(Boolean, nullable=False, default=True)
    armour_class = Column(Integer, nullable=True)
    image = Column(BLOB, nullable=True)

    # 1-n relationships
    race = Column(Integer, ForeignKey("races.id"), nullable=True)
    subrace = Column(Integer, ForeignKey("subraces.id"), nullable=True)
    type_id = Column(Integer, ForeignKey("types.id"), nullable=True)
    size_id = Column(Integer, ForeignKey("sizes.id"), nullable=True)

    # n-n relationships
    parties = relationship(
        "Party",
        secondary="creature_parties",
        back_populates="creatures",
    )
    classes = relationship(
        "Class",
        secondary="creature_classes",
        back_populates="creatures",
        overlaps="subclasses",
    )
    subclasses = relationship(
        "Subclass",
        secondary="creature_classes",
        back_populates="creatures",
        overlaps="classes",
    )
    immunities = relationship("Effect", secondary="creature_immunities")
    resistances = relationship("Effect", secondary="creature_resistances")
    vulnerabilities = relationship("Effect", secondary="creature_vulnerabilities")

    # Relationship references
    creature_type = relationship("Type", back_populates="creatures")
    size = relationship("Size", back_populates="creatures")

    # Polymorph variable
    creature = Column(String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "creatures",
        "polymorphic_on": creature,
    }


class CreatureClasses(Base):
    """
    Cross-reference table for many-to-many relationship between creature, class and subclass.
    """

    __tablename__ = "creature_classes"

    id = Column(Integer, primary_key=True)
    creature_id = Column(Integer, ForeignKey("creatures.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    subclass_id = Column(Integer, ForeignKey("subclasses.id"))


class CreatureParties(Base):
    """
    Cross-reference table for many-to-many relationship between creatures and parties.
    """

    __tablename__ = "creature_parties"

    id = Column(Integer, primary_key=True)
    creature_id = Column("creature_id", Integer, ForeignKey("creatures.id"))
    party_id = Column("party_id", Integer, ForeignKey("parties.id"))


class CreatureResistances(Base):
    """
    Cross-reference table for many-to-many relationship between creature and its resistances.
    """

    __tablename__ = "creature_resistances"

    id = Column(Integer, primary_key=True)
    creature_id = Column("creature_id", Integer, ForeignKey("creatures.id"))
    effect_id = Column("effect_id", Integer, ForeignKey("effects.id"))


class CreatureImmunities(Base):
    """
    Cross-reference table for many-to-many relationship between creature and its immunities.
    """

    __tablename__ = "creature_immunities"

    id = Column(Integer, primary_key=True)
    creature_id = Column("creature_id", Integer, ForeignKey("creatures.id"))
    effect_id = Column("effect_id", Integer, ForeignKey("effects.id"))


class CreatureVulnerabilities(Base):
    """
    Cross-reference table for many-to-many relationship between creature and its vulnerabilities.
    """

    __tablename__ = "creature_vulnerabilities"

    id = Column(Integer, primary_key=True)
    creature_id = Column("creature_id", Integer, ForeignKey("creatures.id"))
    effect_id = Column("effect_id", Integer, ForeignKey("effects.id"))
